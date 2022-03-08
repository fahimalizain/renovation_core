

import unittest
from asyncer import runnify

from pms_app.properties.models import PropertyType, UnitType
from pms_app.properties.controllers.property_type.update import update_property_type
from pms_app.properties.models.property_type.test_property_type import PropertyTypeFixtures
from pms_app.properties.exceptions import PropertyTypeNotFound
import renovation


class TestUpdatePropertyType(unittest.TestCase):

    dt = PropertyType
    property_types = PropertyTypeFixtures()

    @runnify
    async def setUp(self) -> None:
        await self.property_types.setUp()

    @runnify
    async def tearDown(self) -> None:
        await self.property_types.tearDown()

    @runnify
    async def test_update_property_type(self):
        """Test update_property_type controller function"""

        # Get a fixture.
        fixture = self.property_types.fixtures.get(self.dt)[1]
        unit_fixture = self.property_types.get_dependencies(UnitType)[1]

        # Try to update it using wrong name
        with self.assertRaises(PropertyTypeNotFound):
            res = await update_property_type(name="DNE", input={"name": "DNE"})

        # Update it using the controller method

        update = renovation._dict(
            enabled=0,
            title="Test Property Type infinity",
            unit_types=[
                renovation._dict(
                    name=fixture.unit_types[0].name,
                    enabled=1,
                    unit_type=unit_fixture.name
                )
            ]
        )

        res = await update_property_type(
            name=fixture.name,
            input=update
        )

        # Verify it has been updated

        await fixture.reload()
        fixture_dict = fixture.as_dict()

        for field, value in update.items():
            if field == "unit_types":
                continue
            self.assertEqual(value, fixture_dict[field])

        for attribute in fixture.unit_types:  # should be only one
            self.assertEqual(attribute.get("unit_type"), unit_fixture.name)

        # Verify the results
        for attribute in res.unit_types:
            self.assertEqual(attribute.get("unit_type"), unit_fixture.name)
