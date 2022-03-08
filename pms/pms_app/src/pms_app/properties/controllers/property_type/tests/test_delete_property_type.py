
import unittest
from asyncer import runnify

from pms_app.properties.models import PropertyType
from pms_app.properties.controllers.property_type.delete import delete_property_type
from pms_app.properties.models.property_type.test_property_type import PropertyTypeFixtures
from pms_app.properties.exceptions import PropertyTypeNotFound


class TestDeletePropertyType(unittest.TestCase):

    dt = PropertyType
    property_types = PropertyTypeFixtures()

    @runnify
    async def setUp(self) -> None:
        await self.property_types.setUp()

    @runnify
    async def tearDown(self) -> None:
        await self.property_types.tearDown()

    @runnify
    async def test_delete_property_type(self):
        """Test delete_property_type controller function"""

        # Try to update it using wrong name
        with self.assertRaises(PropertyTypeNotFound):
            res = await delete_property_type(name="DNE")

        # Get a fixture
        fixture = self.property_types.fixtures.get(self.dt)[0]

        # Delete it using the controller
        res = await delete_property_type(name=fixture.name)
        self.assertTrue(res)

        # Verify it has been deleted
        self.assertFalse(await PropertyType.get_all(filters=[["name", "=", fixture.name]]))
