from renovation import RenovationModel, _
from .property_type_types import PropertyTypeMeta

from pms_app.properties.exceptions import UnitError
from pms_app.utils import has_table_value_changed


class PropertyType(RenovationModel["PropertyType"], PropertyTypeMeta):
    def before_insert(self):
        self.mirror_has_units_status()

    async def validate(self):

        self.validate_minimum_units()
        await self.validate_unit_types()

    async def on_update(self):

        if not self.flags.in_insert:
            self.mirror_has_units_status()
            self.update_children()
            await self.propagate_changes_to_linked_properties()

    def validate_minimum_units(self):
        """Validate that if it can have units, has at least one"""

        if self.has_units and not self.unit_types:
            raise UnitError(
                _(
                    "Property Type must have at least one Unit Type if 'Has Units' is selected"
                )
            )

    async def validate_unit_types(self):

        for unit_type_item in self.unit_types:
            await unit_type_item.validate_unit_type_enabled()

    def mirror_has_units_status(self):
        """If Has Units is not selected, remove all Unit Types"""

        if self.has_units == 0:
            self.unit_types = []

    async def propagate_changes_to_linked_properties(self):
        """
        Propagate 'enabled' status to all linked Properties
        Remove Units from any linked Properties if Units have unsupported Unit Type
        """
        from ..property.property import Property

        enabled_changes = self.has_value_changed("enabled") and self.enabled == 0

        # Only need to propagate Unit Type changes if item updated or removed
        unit_types_changes = has_table_value_changed(self, "unit_types")
        if not (unit_types_changes.get("removed") or unit_types_changes.get("updated")):
            unit_types_changes = {}

        if enabled_changes or unit_types_changes:

            linked_properties = await Property.get_all(
                filters=[["property_type", "=", self.name]]
            )

            # For every linked property...
            for linked_property in linked_properties:
                property_doc = await Property.get_doc(linked_property.name)

                # Propagate 'active' status
                if self.enabled == 0:
                    property_doc.active = 0
                    await property_doc.save()

                # Propagate supported Unit Types

                removed_rows = unit_types_changes.get("removed")
                updated_rows = unit_types_changes.get("updated")
                changed = False

                # Unit Types that exist on the Property
                existing_types = set([unit.unit_type for unit in property_doc.units])

                updated_unit_list = property_doc.units

                if removed_rows:
                    for removed_item in removed_rows:
                        # If removed Unit Type exists on the Property...
                        if removed_item.unit_type in existing_types:

                            # filter it from the Units
                            updated_unit_list = [
                                unit for unit in updated_unit_list
                                if unit.unit_type != removed_item.unit_type
                            ]

                            changed = True

                if updated_rows:
                    for updated_item in updated_rows:
                        # If updated Unit Type exists on the Property and was disabled
                        if updated_item.get("changes") == [("enabled", 1, 0)] and \
                                updated_item.get("row").unit_type in existing_types:

                            # filter it from the Units
                            updated_unit_list = [
                                unit for unit in updated_unit_list
                                if unit.unit_type != updated_item.get("row").unit_type
                            ]

                            changed = True

                # Save the property with the filtered unit list, if something changed
                if changed:
                    property_doc.units = updated_unit_list
                    await property_doc.save()
