
import unittest
from asyncer import runnify

from pms_app.properties.models import UnitType
from pms_app.properties.controllers.unit_type.create import create_unit_type
from pms_app.properties.models.unit_type.test_unit_type import UnitTypeFixtures


class TestCreateUnitType(unittest.TestCase):

    dt = UnitType
    unitTypes = UnitTypeFixtures()

    @runnify
    async def setUp(self) -> None:
        await self.unitTypes.setUp()

    @runnify
    async def tearDown(self) -> None:
        await self.unitTypes.tearDown()

    @runnify
    async def test_create_unit_type_without_attributes(self):
        """Test create_unit_type controller function without unit attributes"""

        title = "Test Unit infinity"

        # Pass relevant info the create_unit_type
        res = await create_unit_type(
            title=title,
            enabled=True,
        )

        if res:
            self.unitTypes.add_document(res)

        # Verify it has been successfully created
        self.assertTrue(await UnitType.get_all(filters=[["title", "=", title]]))

        doc = await UnitType.get_doc(res.name)

        # Verify the results
        self.assertEqual(doc.title, title)
        self.assertEqual(doc.enabled, 1)
        self.assertEqual(doc.unit_attributes, [])

    @runnify
    async def test_create_unit_type_with_attributes(self):
        """Test create_unit_type controller method with unit attributes"""

        title = "Test Unit infinity"

        # Pass relevant info the create_unit_type
        res = await create_unit_type(
            title=title,
            enabled=True,
            unit_attributes=[
                {
                    "title": "Test Unit 1",
                    "attribute_type": "SELECT",
                    "select_options": "Option1",
                    "default_value": "Option1"
                }
            ]
        )

        if res:
            self.unitTypes.add_document(res)

        # Verify it has been successfully created
        self.assertTrue(await UnitType.get_all(filters=[["title", "=", title]]))

        doc = await UnitType.get_doc(res.name)

        # Verify the results
        self.assertEqual(doc.title, title)
        self.assertEqual(doc.enabled, 1)
        self.assertNotEqual(doc.unit_attributes, [])
