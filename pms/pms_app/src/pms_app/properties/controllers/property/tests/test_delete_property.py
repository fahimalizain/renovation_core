
import unittest
from asyncer import runnify

from pms_app.properties.models import Property
from pms_app.properties.controllers.property.delete import delete_property
from pms_app.properties.models.property.test_property import PropertyFixtures
from pms_app.properties.exceptions import PropertyNotFound


class TestDeleteProperty(unittest.TestCase):

    dt = Property
    properties = PropertyFixtures()

    @runnify
    async def setUp(self) -> None:
        await self.properties.setUp()

    @runnify
    async def tearDown(self) -> None:
        await self.properties.tearDown()

    @runnify
    async def test_delete_property(self):
        """Test delete_property controller function"""

        # Try to delete using wrong name
        with self.assertRaises(PropertyNotFound):
            res = await delete_property(name="DNE")

        # Get a fixture
        property_fixture = self.properties.fixtures.get(self.dt)[0]

        # Delete it using the controller
        res = await delete_property(name=property_fixture.name)
        self.assertTrue(res)

        # Verify it has been deleted
        self.assertFalse(await Property.get_all(filters=[["name", "=", property_fixture.name]]))
