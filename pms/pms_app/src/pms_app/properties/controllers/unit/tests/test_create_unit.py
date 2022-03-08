
import unittest
from asyncer import runnify

import renovation
from pms_app.properties.models import Unit, UnitType, UnitAttributeItem
from pms_app.properties.controllers.unit.create import create_unit
from pms_app.properties.models.unit.test_unit import UnitFixtures


class TestCreateUnit(unittest.TestCase):

    dt = Unit
    units = UnitFixtures()

    @runnify
    async def setUp(self) -> None:
        await self.units.setUp()

    @runnify
    async def tearDown(self) -> None:
        await self.units.tearDown()

    @runnify
    async def test_create_unit_without_attributes(self):
        """Test create_unit controller function without unit attributes"""

        unit_type_fixture = self.units.get_dependencies(UnitType)[0]

        fields = renovation._dict(
            unit_name="Test Unit infinity",
            unit_type=unit_type_fixture.name,
            unit_number=5012,
            description="This is a test unit",
            active=1,
            size=54.2,
        )

        # Pass relevant info the create_unit_type
        res = await create_unit(
            **fields
        )

        if res:
            self.units.add_document(res)

        # Verify it has been successfully created
        self.assertTrue(await Unit.get_all(filters=[["unit_name", "=", fields.unit_name]]))

        # Verify the results
        for field, value in fields.items():
            self.assertEqual(value, res.get(field))

    @runnify
    async def test_create_unit_with_attributes(self):
        """Test create_unit controller method with unit attributes"""

        unit_type_fixture = self.units.get_dependencies(UnitType)[1]

        fields = renovation._dict(
            unit_name="Test Unit infinity",
            unit_type=unit_type_fixture.name,
            unit_number=5012,
            description="This is a test unit",
            active=1,
            size=54.2,
        )

        # Pass relevant info the create_unit_type
        res = await create_unit(
            **fields,
            unit_attributes=[{
                "value": "5",
                "attribute_link": unit_type_fixture.unit_attributes[0].name
            }]
        )

        if res:
            self.units.add_document(res)

        # Verify it has been successfully created
        self.assertTrue(await Unit.get_all(filters=[["unit_name", "=", fields.unit_name]]))

        # Verify the results
        for field, value in fields.items():
            self.assertEqual(value, res.get(field))

        res_attribute = await UnitAttributeItem.get_all(
            filters=[
                ["parent", "=", res.name],
                ["attribute_link", "=", unit_type_fixture.unit_attributes[0].name]
            ],
            fields=["value"]
        )

        self.assertTrue(res_attribute)
        self.assertEqual(res_attribute[0].value, "5")
