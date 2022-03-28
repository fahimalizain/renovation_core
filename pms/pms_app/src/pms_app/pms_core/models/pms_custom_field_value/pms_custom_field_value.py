
import renovation
from renovation import RenovationModel

from .pms_custom_field_value_types import PMSCustomFieldValueMeta
from .exceptions import InvalidValueForSelectField, CustomFieldNotApplicableOnEntityType
from pms_app.pms_core.models.pms_custom_field.pms_custom_field import PMSCustomField
from pms_app.utils.exceptions import NotFound


class PMSCustomFieldValue(RenovationModel["PMSCustomFieldValue"], PMSCustomFieldValueMeta):
    _cf: PMSCustomField = None

    async def validate(self):
        if not await self.get_custom_field():
            raise NotFound(
                message=renovation._("Custom Field: {0} not found").format(self.fieldname)
            )

        await self.validate_entity_type()
        await self.validate_data_field()
        await self.validate_select_field()
        await self.validate_number_field()

    async def get_custom_field(self):
        if self._cf:
            return self._cf

        cf = await PMSCustomField.db_get_value({"fieldname": self.fieldname})
        if not cf:
            return None

        self._cf = await PMSCustomField.get_doc(cf)

        return self._cf

    async def get_fieldtype(self):
        cf = await self.get_custom_field()
        if not cf:
            return None

        return cf.fieldtype

    async def get_options(self):
        cf = await self.get_custom_field()
        if not cf:
            return None

        return cf.options or ""

    async def validate_entity_type(self):
        cf = await self.get_custom_field()
        if self.entity_type not in cf.get_applicable_entity_types():
            raise CustomFieldNotApplicableOnEntityType(
                cf_label=cf.label, cf_fieldname=cf.fieldname,
                valid_entity_types=cf.get_applicable_entity_types(),
                current_type=self.entity_type
            )

    async def validate_data_field(self):
        # 👀👀
        if await self.get_fieldtype() != "Data":
            return

        self.value = str(self.value or "")

    async def validate_select_field(self):
        if await self.get_fieldtype() != "Select":
            return

        options = (await self.get_options()).split("\n")
        value = str(self.value or "").strip()

        if value not in options:
            raise InvalidValueForSelectField(
                fieldname=self.fieldname, options=options, value=value
            )

        self.value = value

    async def validate_number_field(self):
        fieldtype = await self.get_fieldtype()

        if fieldtype == "Float":
            value = renovation.flt(self.value)
        elif fieldtype == "Integer":
            value = renovation.cint(self.value)
        else:
            return

        self.value = str(value)
