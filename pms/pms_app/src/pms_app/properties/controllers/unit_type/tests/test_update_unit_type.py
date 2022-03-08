
import unittest
from asyncer import runnify

import renovation
from pms_app.properties.models import UnitType
from pms_app.properties.controllers.unit_type.update import update_unit_type
from pms_app.properties.models.unit_type.test_unit_type import UnitTypeFixtures
from pms_app.properties.exceptions import UnitTypeNotFound


class TestUpdateUnitType(unittest.TestCase):

    dt = UnitType
    unitTypes = UnitTypeFixtures()

    @runnify
    async def setUp(self) -> None:
        await self.unitTypes.setUp()

    @runnify
    async def tearDown(self) -> None:
        await self.unitTypes.tearDown()

    @runnify
    async def test_update_unit_type(self):
        """Test update_unit_type controller function"""

        # Get a fixture
        fixture = self.unitTypes.fixtures.get(UnitType)[0]

        # Try to update it using wrong name
        with self.assertRaises(UnitTypeNotFound):
            res = await update_unit_type(name="DNE", input={"name": "DNE"})

        # Update it using the controller method
        # Add new Unit Attribute as well as update

        attribute_name = fixture.unit_attributes[0].name

        update = renovation._dict(
            title="New name",
            enabled="0",
            unit_attributes=[
                renovation._dict(
                    name=attribute_name,
                    title="Updated attribute title",
                    attribute_type="NUMBER",
                    select_options="",
                    default_value="-94",
                ),
                renovation._dict(
                    title="New attribute",
                    attribute_type="DATA",
                    select_options="",
                    default_value="1",
                )
            ]
        )

        res = await update_unit_type(
            name=fixture.name,
            input=update
        )

        # Verify it has been updated

        await fixture.reload()
        fixture_dict = fixture.as_dict()

        for field, value in update.items():
            if field == "unit_attributes":
                continue
            self.assertEqual(value, str(fixture_dict[field]))

        for attribute in fixture.unit_attributes:
            if attribute.get("name") == attribute_name:
                self.assertEqual(attribute.get("title"), "Updated attribute title")
                self.assertEqual(attribute.get("attribute_type"), "Number")
                self.assertEqual(attribute.get("select_options"), "")
                self.assertEqual(attribute.get("default_value"), "-94")
            else:
                self.assertEqual(attribute.get("title"), "New attribute")
                self.assertEqual(attribute.get("attribute_type"), "Data")
                self.assertEqual(attribute.get("select_options"), "")
                self.assertEqual(attribute.get("default_value"), "1")

        # Verify the results
        for attribute in res.unit_attributes:
            if attribute.get("name") == attribute_name:
                self.assertEqual(attribute.get("title"), "Updated attribute title")
                self.assertEqual(attribute.get("attribute_type"), "Number")
                self.assertEqual(attribute.get("select_options"), "")
                self.assertEqual(attribute.get("default_value"), "-94")
            else:
                self.assertEqual(attribute.get("title"), "New attribute")
                self.assertEqual(attribute.get("attribute_type"), "Data")
                self.assertEqual(attribute.get("select_options"), "")
                self.assertEqual(attribute.get("default_value"), "1")
