
import unittest
from asyncer import runnify

from pms_app.properties.models import Unit
from pms_app.properties.controllers.unit.delete import delete_unit
from pms_app.properties.models.unit.test_unit import UnitFixtures


class TestDeleteUnit(unittest.TestCase):

    dt = Unit
    units = UnitFixtures()

    @runnify
    async def setUp(self) -> None:
        await self.units.setUp()

    @runnify
    async def tearDown(self) -> None:
        await self.units.tearDown()

    @runnify
    async def test_delete_unit(self):
        """Test delete_unit controller function"""

        # Get a fixture
        fixture = self.units.fixtures.get(self.dt)[0]

        # Delete it using the controller
        res = await delete_unit(name=fixture.name)
        self.assertTrue(res)

        # Verify it has been deleted
        self.assertFalse(await Unit.get_all(filters=[["name", "=", fixture.name]]))
