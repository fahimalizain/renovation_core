# Copyright (c) 2021, Leam Technology Systems and Contributors
# See license.txt

import unittest
from asyncer import runnify

import renovation
from renovation.tests import RenovationTestFixture
from pms_app.properties.exceptions import UnitAttributeError

from .unit_type import UnitType
from ..unit.unit import Unit
from ..unit_type_attribute_item.unit_type_attribute_item import UnitTypeAttributeItem


class UnitTypeFixtures(RenovationTestFixture):

    def __init__(self):
        super().__init__()
        self.DEFAULT_MODEL = UnitType

    async def make_fixtures(self):

        fix_1 = UnitType(renovation._dict(
            title="Test UnitType 1",
            enabled=1,
            unit_attributes=[
                renovation._dict(
                    title="Test Attribute 1",
                    attribute_type="Select",
                    select_options="1\n2",
                    default_value="1"
                ),
                renovation._dict(
                    title="Test Attribute 2",
                    attribute_type="Multi-Select",
                    select_options="1\n2",
                    default_value="1"
                ),
                renovation._dict(
                    title="Test Attribute 3",
                    attribute_type="Data",
                    default_value="Test"
                ),
                renovation._dict(
                    title="Test Attribute 4",
                    attribute_type="Number",
                    default_value="5466"
                )
            ]
        ))
        await fix_1.insert()
        self.add_document(fix_1)

        fix_2 = UnitType(renovation._dict(
            title="Test UnitType 2",
            enabled=1,
            unit_attributes=[
                renovation._dict(
                    title="Test Attribute 1",
                    attribute_type="Data",
                    default_value="Test"
                ),
                renovation._dict(
                    title="Test Attribute 2",
                    attribute_type="Number",
                    default_value="5466"
                ),
                renovation._dict(
                    title="Test Attribute 3",
                    attribute_type="Data",
                    default_value="Test"
                ),
                renovation._dict(
                    title="Test Attribute 4",
                    attribute_type="Number",
                    default_value="5466"
                )
            ]
        ))
        await fix_2.insert()
        self.add_document(fix_2)


class TestUnitType(unittest.TestCase):

    dt = UnitType
    unitTypes = UnitTypeFixtures()

    @runnify
    async def setUp(self) -> None:
        await self.unitTypes.setUp()

    @runnify
    async def tearDown(self) -> None:
        await self.unitTypes.tearDown()

    @runnify
    async def test_unit_type_set_disabled_propagates_to_units(self):
        """Test that if a Unit Type is disabled, all linked Units also become disabled"""

        unit_type_fixture = self.unitTypes.fixtures.get(self.dt)[0]

        # First create some test docs that are linked to the Unit Type
        unit1 = Unit({
            "unit_name": "Test Unit 1",
            "unit_type": unit_type_fixture.name,
            "active": 1,
        })
        await unit1.insert()

        unit2 = Unit({
            "unit_name": "Test Unit 2",
            "unit_type": unit_type_fixture.name,
            "active": 0,
        })
        await unit2.insert()

        # Make some active, some deactivated; verify

        self.assertEqual(unit1.active, 1)
        self.assertEqual(unit2.active, 0)

        # Disable the Unit Type, and verify that they are all disabled

        unit_type_fixture.enabled = 0
        await unit_type_fixture.save()
        await unit1.reload()
        await unit2.reload()

        self.assertEqual(unit1.active, 0)
        self.assertEqual(unit2.active, 0)

        # Enable the Unit Type, and verify that they remain disabled

        unit_type_fixture.enabled = 1
        await unit_type_fixture.save()
        await unit1.reload()
        await unit2.reload()

        self.assertEqual(unit1.active, 0)
        self.assertEqual(unit2.active, 0)

        # Need to delete them directly; leaving to tearDown produces errors
        await unit1.delete()
        await unit2.delete()

    @runnify
    async def test_unit_type_attribute_change_propagation_to_units(self):
        """Test that if Unit Type attributes change, all linked Units attributes also change"""

        unit_type_fixture = self.unitTypes.fixtures.get(self.dt)[0]

        # First create some test docs that are linked to fixture
        unit1 = Unit({
            "unit_name": "Test Unit 1",
            "unit_type": unit_type_fixture.name,
            "active": 1,
        })
        await unit1.insert()
        await unit1.reload()

        unit2 = Unit({
            "unit_name": "Test Unit 2",
            "unit_type": unit_type_fixture.name,
            "active": 0,
        })
        await unit2.insert()
        await unit2.reload()

        # Verify that they have the same unit attributes as the Unit Type
        unit_type_attributes = [attribute.name for attribute in unit_type_fixture.unit_attributes]
        unit1_unit_attributes = [attribute.attribute_link for attribute in unit1.unit_attributes]
        unit2_unit_attributes = [attribute.attribute_link for attribute in unit2.unit_attributes]

        self.assertEqual(unit_type_attributes, unit1_unit_attributes)
        self.assertEqual(unit_type_attributes, unit2_unit_attributes)

        # Make modifications to the Unit Type attributes
        unit_type_fixture.unit_attributes = []
        await unit_type_fixture.save()
        await unit1.reload()
        await unit2.reload()

        # Verify that they are propagated
        unit_type_attributes = [attribute.name for attribute in unit_type_fixture.unit_attributes]
        unit1_unit_attributes = [attribute.attribute_link for attribute in unit1.unit_attributes]
        unit2_unit_attributes = [attribute.attribute_link for attribute in unit2.unit_attributes]

        self.assertEqual(unit_type_attributes, unit1_unit_attributes)
        self.assertEqual(unit_type_attributes, unit2_unit_attributes)

        # Need to delete them directly; leaving to tearDown produces errors
        await unit1.delete()
        await unit2.delete()

    # Unit Attribute Testing

    @runnify
    async def test_data_attribute_value_cannot_be_multiline(self):
        """Test that the default value for Data attributes cannot be multiline"""

        # Get a fixture
        unit_fixture = self.unitTypes.fixtures.get(self.dt)[0]

        # Add a Data type attribute to it with invalid default_value

        attribute_item = UnitTypeAttributeItem(renovation._dict(
            title="Test Attribute 1",
            attribute_type="Data",
            select_options="",
            default_value="1\n2"
        ))

        unit_fixture.unit_attributes = [
            attribute_item
        ]

        # Verify it fails
        with self.assertRaises(UnitAttributeError):
            await unit_fixture.save()

    @runnify
    async def test_number_attribute_value_cannot_be_multiline(self):
        """Test that the default value for Number attributes cannot be multiline"""

        # Get a fixture
        unit_fixture = self.unitTypes.fixtures.get(self.dt)[0]

        # Add a Number type attribute to it with a multi-line default_value

        attribute_item = UnitTypeAttributeItem(renovation._dict(
            title="Test Attribute 1",
            attribute_type="Number",
            select_options="",
            default_value="1\n2"
        ))

        unit_fixture.unit_attributes = [
            attribute_item
        ]

        # Verify it fails
        with self.assertRaises(UnitAttributeError):
            await unit_fixture.save()

    @runnify
    async def test_number_attribute_value_cannot_be_non_numeric(self):
        """Test that the default value for Number attributes cannot be non-numeric"""

        # Get a fixture
        unit_fixture = self.unitTypes.fixtures.get(self.dt)[0]

        # Add a Number type attribute to it with a multi-line default_value

        attribute_item = UnitTypeAttributeItem(renovation._dict(
            title="Test Attribute 1",
            attribute_type="Number",
            select_options="",
            default_value="non"
        ))

        unit_fixture.unit_attributes = [
            attribute_item
        ]

        # Verify it fails
        with self.assertRaises(UnitAttributeError):
            await unit_fixture.save()

    @runnify
    async def test_select_attribute_value_cannot_be_multiline(self):
        """Test that the default value for Select attributes cannot be multiline"""

        # Get a fixture
        unit_fixture = self.unitTypes.fixtures.get(self.dt)[0]

        # Add a Select type attribute to it with a multi-line default_value

        attribute_item = UnitTypeAttributeItem(renovation._dict(
            title="Test Attribute 1",
            attribute_type="Select",
            select_options="1\n2",
            default_value="1\n2"
        ))

        unit_fixture.unit_attributes = [
            attribute_item
        ]

        # Verify it fails
        with self.assertRaises(UnitAttributeError):
            await unit_fixture.save()

    @runnify
    async def test_select_attribute_value_cannot_be_a_value_not_in_options(self):
        """
        Test that the default value for Select attributes cannot be
        a value that does not exist in the options
        """

        # Get a fixture
        unit_fixture = self.unitTypes.fixtures.get(self.dt)[0]

        # Add a Select type attribute to it with a multi-line default_value

        attribute_item = UnitTypeAttributeItem(renovation._dict(
            title="Test Attribute 1",
            attribute_type="Select",
            select_options="1\n2",
            default_value="non"
        ))

        unit_fixture.unit_attributes = [
            attribute_item
        ]

        # Verify it fails
        with self.assertRaises(UnitAttributeError):
            await unit_fixture.save()

    @runnify
    async def test_multiselect_attribute_value_cannot_be_a_value_not_in_options(self):
        """
        Test that the default value for Multi-Select attributes
        cannot be a value that does not exist in the options
        """

        # Get a fixture
        unit_fixture = self.unitTypes.fixtures.get(self.dt)[0]

        # Add a Select type attribute to it with a default_value that does not exist in the options

        attribute_item = UnitTypeAttributeItem(renovation._dict(
            title="Test Attribute 1",
            attribute_type="Select",
            select_options="1\n2",
            default_value="3"
        ))

        unit_fixture.unit_attributes = [
            attribute_item
        ]

        # Verify it fails
        with self.assertRaises(UnitAttributeError):
            await unit_fixture.save()

    @runnify
    async def test_select_attribute_needs_options(self):
        """Test that if an attribute is of the type Select it needs options"""

        unit_type = UnitType(renovation._dict(
            title="Test UnitType infinity",
            unit_attributes=[
                renovation._dict(
                    title="Test Attribute 1",
                    attribute_type="Select",
                    default_value="Option 1"
                )
            ]
        ))

        # Select with no options should fail
        with self.assertRaises(UnitAttributeError):
            await unit_type.insert()

    @runnify
    async def test_select_attribute_needs_unique_options(self):
        """Test that if an attribute is of the type Select options must be unique"""

        unit_type = UnitType(renovation._dict(
            title="Test UnitType infinity",
            unit_attributes=[
                renovation._dict(
                    title="Test Attribute 1",
                    attribute_type="Select",
                    default_value="Option 1\nOption 1"
                )
            ]
        ))

        # Select with non-unique options should fail
        with self.assertRaises(UnitAttributeError):
            await unit_type.insert()

    @runnify
    async def test_multiselect_attribute_needs_options(self):
        """Test that if an attribute is of the type Multi-Select it needs options"""

        unit_type = UnitType(renovation._dict(
            title="Test UnitType infinity",
            unit_attributes=[
                renovation._dict(
                    title="Test Attribute 1",
                    attribute_type="Multi-Select",
                    default_value="Option 1"
                )
            ]
        ))

        # Multi-Select with no options should fail
        with self.assertRaises(UnitAttributeError):
            await unit_type.insert()

    @runnify
    async def test_multiselect_attribute_needs_unique_options(self):
        """Test that if an attribute is of the type Multi-Select options must be unique"""

        unit_type = UnitType(renovation._dict(
            title="Test UnitType infinity",
            unit_attributes=[
                renovation._dict(
                    title="Test Attribute 1",
                    attribute_type="Multi-Select",
                    default_value="Option 1\nOption 1"
                )
            ]
        ))

        # Multi-Select with non unique options should fail
        with self.assertRaises(UnitAttributeError):
            await unit_type.insert()
