
import unittest
from asyncer import runnify

from pms_app.properties.models import UnitType
from pms_app.properties.controllers.unit_type.delete import delete_unit_type
from pms_app.properties.models.unit_type.test_unit_type import UnitTypeFixtures


class TestDeleteUnitType(unittest.TestCase):

    dt = UnitType
    unitTypes = UnitTypeFixtures()

    @runnify
    async def setUp(self) -> None:
        await self.unitTypes.setUp()

    @runnify
    async def tearDown(self) -> None:
        await self.unitTypes.tearDown()

    @runnify
    async def test_delete_unit_type(self):
        """Test delete_unit_type controller function"""

        # Get a fixture
        fixture = self.unitTypes.fixtures.get(UnitType)[0]

        # Delete it using the controller
        res = await delete_unit_type(name=fixture.name)
        self.assertTrue(res)
        # Verify it has been deleted
        self.assertFalse(await UnitType.get_all(filters=[["name", "=", fixture.name]]))
