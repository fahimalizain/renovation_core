
import unittest
from asyncer import runnify

import renovation
from pms_app.properties.controllers.property.create import create_property
from pms_app.properties.models import Property, PropertyType, Unit, UnitItem
from pms_app.properties.models.property.test_property import PropertyFixtures


class TestCreateProperty(unittest.TestCase):

    dt = Property
    properties = PropertyFixtures()

    @runnify
    async def setUp(self) -> None:
        await self.properties.setUp()

    @runnify
    async def tearDown(self) -> None:
        await self.properties.tearDown()

    @runnify
    async def test_create_property(self):
        """Test create_property controller method"""

        property_type_fixture = self.properties.get_dependencies(PropertyType)[0]
        property_fixture = self.properties.fixtures.get(self.dt)[0]
        unit = self.properties.get_dependencies(Unit)[0]

        fields = renovation._dict(
            active=1,
            property_name="Test Property infinity",
            property_type=property_type_fixture.name,
            description="This is a test",
            city="Abu Dubai",
            beneficiary=property_fixture.beneficiary,
            units=[
                {
                    "unit": unit.name
                }
            ]
        )

        # Pass relevant info the create_property_type
        res = await create_property(
            **fields,
        )

        if res:
            self.properties.add_document(res)

        # Verify it has been successfully created
        self.assertTrue(await Property.get_all(filters=[
                        ["property_name", "=", fields.property_name]]))

        # Verify the results
        for field, value in fields.items():
            if field == "units":
                continue
            self.assertEqual(value, res.get(field))

        res_attribute = await UnitItem.get_all(
            filters=[
                ["parent", "=", res.name],
                ["unit", "=", unit.name]
            ],
        )

        self.assertTrue(res_attribute)
