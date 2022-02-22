from renovation import RenovationModel, _

from pms_app.properties.exceptions import PropertyTypeNotEnabled, UnitError, UnitItemError


class Property(RenovationModel["Property"]):
    async def validate(self):

        await self.validate_property_type()
        await self.validate_units()

    async def validate_units(self):

        for unit in self.units:
            await self.validate_unique_unit(unit)
            await self.validate_unit_type_of_unit(unit)

    async def validate_property_type(self):
        """Validate that if self is active, only enabled Property Types can be added"""
        from .property_type import PropertyType

        if self.active:
            property_type = await PropertyType.get_doc(self.property_type)
            if not property_type.enabled:
                raise PropertyTypeNotEnabled(
                    _(
                        "A disabled Property Type cannot be added to an active Property"
                    )
                )

    async def validate_unique_unit(self, unit_item):
        """Validate that a Unit can only exist on one Property"""
        from .unit_item import UnitItem

        unit_items = await UnitItem.get_all(
            filters=[
                ["unit", "=", unit_item.unit],
                ["parent", "!=", self.name]
            ],
            fields=["parent"]
        )

        if unit_items:
            raise UnitError(
                _(
                    "Error adding Unit No. {0}. '{1}'. This Unit already exists on Property '{2}'"
                ).format(unit_item.idx, unit_item.unit, unit_items[0].parent)
            )

    async def validate_unit_type_of_unit(self, unit_item):
        """Validate that only Units with Unit Types that exist on the Property Type are allowed"""
        from .property_type import PropertyType
        property_type_doc = await PropertyType.get_doc(self.property_type)

        supported_unit_types = set([
            unit_type_item.unit_type for unit_type_item in property_type_doc.unit_types
        ])

        for unit_item in self.units:
            if unit_item.unit_type not in supported_unit_types:
                raise UnitItemError(
                    _(
                        "Unit No. {0}: '{1}' has a Unit Type of '{2}' which is not "
                        "supported by Property Type '{3}'"
                    ).format(
                        unit_item.idx, unit_item.unit, unit_item.unit_type, self.property_type
                    )
                )
