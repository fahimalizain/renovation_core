
import unittest
from asyncer import runnify

import renovation
from pms_app.properties.models import Unit, UnitType
from pms_app.properties.controllers.unit.update import update_unit
from pms_app.properties.models.unit.test_unit import UnitFixtures
from pms_app.properties.exceptions import UnitNotFound


class TestUpdateUnit(unittest.TestCase):

    dt = Unit
    units = UnitFixtures()

    @runnify
    async def setUp(self) -> None:
        await self.units.setUp()

    @runnify
    async def tearDown(self) -> None:
        await self.units.tearDown()

    @runnify
    async def test_update_unit(self):
        """Test update_unit controller function"""

        # Get a fixture
        unit_type_fixture = self.units.get_dependencies(UnitType)[1]
        fixture = self.units.fixtures.get(self.dt)[2]

        # Try to update it using wrong name
        with self.assertRaises(UnitNotFound):
            res = await update_unit(name="DNE", input={"name": "DNE"})

        # Update it using the controller method
        # Add new Unit Attribute as well as update

        attribute_link_name = fixture.unit_attributes[0].attribute_link

        update = renovation._dict(
            unit_name="Test Unit infinity",
            unit_type=unit_type_fixture.name,
            unit_number=5012,
            description="This is a test unit",
            active=1,
            size=54.2,
            unit_attributes=[
                renovation._dict(
                    name=fixture.unit_attributes[0].name,
                    attribute_link=attribute_link_name,
                    value="-94",
                )
            ]
        )

        res = await update_unit(
            name=fixture.name,
            input=update
        )

        # Verify it has been updated

        await fixture.reload()
        fixture_dict = fixture.as_dict()

        for field, value in update.items():
            if field == "unit_attributes":
                continue
            self.assertEqual(value, fixture_dict[field])

        for attribute in fixture.unit_attributes:
            if attribute.get("attribute_link") == attribute_link_name:
                self.assertEqual(attribute.get("value"), "-94")

        # Verify the results
        for attribute in res.unit_attributes:
            if attribute.get("attribute_link") == attribute_link_name:
                self.assertEqual(attribute.get("value"), "-94")
