from renovation import RenovationModel, _
from pms_app.properties.exceptions import UnitTypeNotFound


class Unit(RenovationModel["Unit"]):
    async def before_insert(self):
        await self.copy_attributes_from_unit_type()

    async def validate(self):

        await self.validate_enabled_unit_type()
        if self.flags.in_insert:
            self.validate_unit_attributes()  # For save(), validate separately

    async def on_change(self):

        if self.has_value_changed("unit_type"):
            await self.update_property_unit_items()

        # If not in insert, copy the attributes from the Unit Type
        # Set a flag before the save and reset it after to avoid recursive save() calls

        if not self.flags.in_insert and not self.flags.saving_attributes:
            self.flags.saving_attributes = True

            await self.copy_attributes_from_unit_type(set_name=True)
            self.validate_unit_attributes()  # Run previously ignored validation
            self.save()

        if self.flags.saving_attributes:
            self.flags.saving_attributes = False

    async def copy_attributes_from_unit_type(self, set_name=False):
        from .unit_type import UnitType

        unit_type = await UnitType.get_doc(self.unit_type)
        for type_attribute in unit_type.unit_attributes:

            existing_row = [
                attribute_row for attribute_row in self.unit_attributes
                if attribute_row.attribute_link == type_attribute.name
            ]

            if existing_row:
                existing_row = existing_row[0]
                existing_row.title = type_attribute.title
                existing_row.attribute_type = type_attribute.attribute_type
                existing_row.select_options = type_attribute.select_options
            else:
                self.append("unit_attributes", {
                    "title": type_attribute.title,
                    "attribute_type": type_attribute.attribute_type,
                    "value": type_attribute.default_value,
                    "attribute_link": type_attribute.name,
                    "select_options": type_attribute.select_options
                })

    async def validate_enabled_unit_type(self):
        """Validate that only an enabled Unit Type can be added, if self is set to active"""
        from .unit_type import UnitType
        unit_type = await UnitType.get_doc(self.unit_type)

        if not unit_type.enabled and self.active:
            raise UnitTypeNotFound(
                _(
                    "The linked Unit Type '{0}' is not enabled"
                ).format(unit_type.name)
            )

    def validate_unit_attributes(self):
        """Validate the list of Unit Attributes"""

        for attribute in self.unit_attributes:
            attribute.validate_unit_attribute_on_linked_unit_type(self)
            attribute.validate_unit_attribute_value_type()

    async def update_property_unit_items(self):
        """Update the Unit Items on Properties containing this Unit"""
        from .unit_item import UnitItem
        linked_unit_items = await UnitItem.get_all(
            filters=[["unit", "=", self.name]]
        )

        for linked_unit_item in linked_unit_items:
            await UnitItem.db_set_value(linked_unit_item.name, "unit_type", self.unit_type)
