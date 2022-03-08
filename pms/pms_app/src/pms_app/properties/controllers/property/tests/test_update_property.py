
import unittest
from asyncer import runnify

import renovation
from pms_app.properties.models import Unit, PropertyType, Property
from pms_app.properties.controllers.property.update import update_property
from pms_app.properties.models.property.test_property import PropertyFixtures
from pms_app.properties.exceptions import PropertyNotFound


class TestUpdateProperty(unittest.TestCase):

    dt = Property
    properties = PropertyFixtures()

    @runnify
    async def setUp(self) -> None:
        await self.properties.setUp()

    @runnify
    async def tearDown(self) -> None:
        await self.properties.tearDown()

    @runnify
    async def test_update_property(self):
        """Test update_property controller function"""

        # Get a fixture
        property_type_fixture = self.properties.get_dependencies(PropertyType)[0]
        property_fixture = self.properties.fixtures.get(self.dt)[0]
        unit = self.properties.get_dependencies(Unit)[0]

        # Try to update it using wrong name
        with self.assertRaises(PropertyNotFound):
            res = await update_property(name="DNE", input={"name": "DNE"})

        # Update it using the controller method
        # Add new Property Attribute as well as update

        update = renovation._dict(
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

        res = await update_property(
            name=property_fixture.name,
            input=update
        )

        # Verify it has been updated

        await property_fixture.reload()
        fixture_dict = property_fixture.as_dict()

        for field, value in update.items():
            if field == "units":
                continue
            self.assertEqual(value, fixture_dict[field])

        for attribute in property_fixture.units:
            self.assertEqual(attribute.get("unit"), unit.name)  # Only one

        # Verify the results
        for attribute in res.units:
            self.assertEqual(attribute.get("unit"), unit.name)
