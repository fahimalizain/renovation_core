

import unittest
from asyncer import runnify

import renovation
from pms_app.properties.models import PropertyType, UnitType, UnitTypeItem
from pms_app.properties.controllers.property_type.create import create_property_type
from pms_app.properties.models.property_type.test_property_type import PropertyTypeFixtures


class TestCreatePropertyType(unittest.TestCase):

    dt = PropertyType
    property_types = PropertyTypeFixtures()

    @runnify
    async def setUp(self) -> None:
        await self.property_types.setUp()

    @runnify
    async def tearDown(self) -> None:
        await self.property_types.tearDown()

    @runnify
    async def test_create_property_type(self):
        """Test create_property_type controller method"""

        unit_type_fixture = self.property_types.get_dependencies(UnitType)[0]

        fields = renovation._dict(
            enabled=1,
            title="Test Property Type infinity",
            has_units=1,
        )

        # Pass relevant info the create_property_type_type
        res = await create_property_type(
            **fields,
            unit_types=[
                renovation._dict(
                    enabled=1,
                    unit_type=unit_type_fixture.name,
                )
            ]
        )

        if res:
            self.property_types.add_document(res)

        # Verify it has been successfully created
        self.assertTrue(await PropertyType.get_all(filters=[["title", "=", fields.title]]))

        # Verify the results
        for field, value in fields.items():
            if field == "unit_types":
                continue
            self.assertEqual(value, res.get(field))

        res_attribute = await UnitTypeItem.get_all(
            filters=[
                ["parent", "=", res.name],
                ["unit_type", "=", unit_type_fixture.name]
            ],
            fields=["enabled"]
        )

        self.assertTrue(res_attribute)
        self.assertEqual(int(res_attribute[0].enabled), 1)
