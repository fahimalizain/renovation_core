
from renovation import RenovationModel, scrub
import renovation

from .pms_custom_field_types import PMSCustomFieldMeta
from .exceptions import InvalidCustomFieldOption, NonCustomizableEntityType, DuplicateFieldname

CF_FIELDNAME_PREFIX = "pmscf_"


class PMSCustomField(RenovationModel["PMSCustomField"], PMSCustomFieldMeta):
    """
    - FieldType updates are allowed with no restrictions
    """

    async def validate(self):
        if not self.fieldname:
            self.fieldname = CF_FIELDNAME_PREFIX + scrub(self.label)

        self.validate_customizable_entity_type()
        await self.validate_unique_fieldname()
        self.validate_data_field()
        self.validate_select_field()
        self.validate_no_options_specified()

    def validate_customizable_entity_type(self):
        if not self.entity_type:
            return

        entity_types = set(renovation.get_hooks("pms_customizable_entity_types"))
        if self.entity_type not in entity_types:
            raise NonCustomizableEntityType(entity_type=self.entity_type)

    async def validate_unique_fieldname(self):
        # Test uniqueness with existing Custom Fields
        entity_types = self.get_applicable_entity_types()
        custom_fields = await PMSCustomField.get_all(
            dict(fieldname=self.fieldname))

        for cf in custom_fields:
            if cf.name == self.name:
                continue

            cf = await PMSCustomField.get_doc(cf.name)
            cf_entity_types = set(cf.get_applicable_entity_types())

            common_entities = list(cf_entity_types.intersection(entity_types))
            if len(common_entities) > 0:
                raise DuplicateFieldname(
                    fieldname=self.fieldname, fieldtype=self.fieldtype, options=self.options,
                    entity_type=common_entities[0]
                )

        for entity_type in self.get_applicable_entity_types():
            meta = renovation.get_meta(entity_type)
            if meta.get_field(self.fieldname):
                raise DuplicateFieldname(
                    fieldname=self.fieldname, fieldtype=self.fieldtype, options=self.options,
                    entity_type=entity_type
                )

    def validate_data_field(self):
        if self.fieldtype != "Data":
            return

        if not self.options:
            return

        data_field_options = (
            'Email',
            'Name',
            'Phone',
            'URL',
            'Barcode'
        )

        if self.options not in data_field_options:
            raise InvalidCustomFieldOption(
                fieldname=self.fieldname,
                fieldtype=self.fieldtype,
                options=self.options,
                message=renovation._("Data field can only have these options: {0}").format(
                    ", ".join(data_field_options)))

    def validate_select_field(self):
        if self.fieldtype != "Select":
            return

        if not self.options:
            raise InvalidCustomFieldOption(
                fieldname=self.fieldname,
                fieldtype=self.fieldtype,
                options=self.options,
                message=renovation._("Select fields require options"))

        options = self.options.split("\n")
        self.options = "\n".join([x.strip() for x in options])

    def validate_no_options_specified(self):
        if self.fieldtype not in ("Integer", "Float"):
            return

        if self.options:
            raise InvalidCustomFieldOption(
                fieldname=self.fieldname,
                fieldtype=self.fieldtype,
                options=self.options,
                message=renovation._("{0} fields cannot have options").format(self.fieldtype))

    def get_applicable_entity_types(self):
        if self.entity_type:
            return [self.entity_type]

        # Global
        entities_excluded = [x.model for x in self.entities_excluded]

        # Customizable Doctypes
        customizable_types = set(renovation.get_hooks("pms_customizable_entity_types"))
        customizable_types.difference_update(entities_excluded)
        return list(customizable_types)
