# Copyright (c) 2021, Leam Technology Systems and Contributors
# See license.txt

import unittest

import frappe
from frappe_testing.test_fixture import TestFixture
from pms_app.properties.exceptions import UnitAttributeError


class UnitTypeFixtures(TestFixture):

    def __init__(self):
        super().__init__()
        self.DEFAULT_DOCTYPE = "Unit Type"

    def make_fixtures(self):

        fix_1 = frappe.get_doc(frappe._dict(
            doctype=self.DEFAULT_DOCTYPE,
            title="Test UnitType 1",
            enabled=1,
            unit_attributes=[
                frappe._dict(
                    title="Test Attribute 1",
                    attribute_type="Select",
                    select_options="1\n2",
                    default_value="1"
                ),
                frappe._dict(
                    title="Test Attribute 2",
                    attribute_type="Multi-Select",
                    select_options="1\n2",
                    default_value="1"
                ),
                frappe._dict(
                    title="Test Attribute 3",
                    attribute_type="Data",
                    default_value="Test"
                ),
                frappe._dict(
                    title="Test Attribute 4",
                    attribute_type="Number",
                    default_value="5466"
                )
            ]
        )).insert()

        fix_1.reload()
        self.add_document(fix_1)

        fix_2 = frappe.get_doc(frappe._dict(
            doctype=self.DEFAULT_DOCTYPE,
            title="Test UnitType 2",
            enabled=1,
            unit_attributes=[
                frappe._dict(
                    title="Test Attribute 1",
                    attribute_type="Data",
                    default_value="Test"
                ),
                frappe._dict(
                    title="Test Attribute 2",
                    attribute_type="Number",
                    default_value="5466"
                ),
                frappe._dict(
                    title="Test Attribute 3",
                    attribute_type="Data",
                    default_value="Test"
                ),
                frappe._dict(
                    title="Test Attribute 4",
                    attribute_type="Number",
                    default_value="5466"
                )
            ]
        )).insert()

        fix_2.reload()
        self.add_document(fix_2)


class TestUnitType(unittest.TestCase):

    dt = "Unit Type"
    unitTypes = UnitTypeFixtures()

    def setUp(self) -> None:
        self.unitTypes.setUp()

    def tearDown(self) -> None:
        self.unitTypes.tearDown()

    def test_unit_type_set_disabled_propagates_to_units(self):
        """Test that if a Unit Type is disabled, all linked Units also become disabled"""

        unit_type_fixture = self.unitTypes.fixtures.get(self.dt)[0]

        # First create some test docs that are linked to the Unit Type
        unit1 = frappe.get_doc({
            "doctype": "Unit",
            "unit_name": "Test Unit 1",
            "unit_type": unit_type_fixture.name,
            "active": 1,
        }).insert()

        unit2 = frappe.get_doc({
            "doctype": "Unit",
            "unit_name": "Test Unit 2",
            "unit_type": unit_type_fixture.name,
            "active": 0,
        }).insert()

        # Make some active, some deactivated; verify

        self.assertEqual(unit1.active, 1)
        self.assertEqual(unit2.active, 0)

        # Disable the Unit Type, and verify that they are all disabled

        unit_type_fixture.enabled = 0
        unit_type_fixture.save()
        unit_type_fixture.reload()
        unit1.reload()
        unit2.reload()

        self.assertEqual(unit1.active, 0)
        self.assertEqual(unit2.active, 0)

        # Enable the Unit Type, and verify that they remain disabled

        unit_type_fixture.enabled = 1
        unit_type_fixture.save()
        unit_type_fixture.reload()
        unit1.reload()
        unit2.reload()

        self.assertEqual(unit1.active, 0)
        self.assertEqual(unit2.active, 0)

        # Need to delete them directly; leaving to tearDown produces errors
        frappe.delete_doc("Unit", unit1.name, delete_permanently=True)
        frappe.delete_doc("Unit", unit2.name, delete_permanently=True)

    def test_unit_type_attribute_change_propagation_to_units(self):
        """Test that if Unit Type attributes change, all linked Units attributes also change"""

        unit_type_fixture = self.unitTypes.fixtures.get(self.dt)[0]

        # First create some test docs that are linked to fixture
        unit1 = frappe.get_doc({
            "doctype": "Unit",
            "unit_name": "Test Unit 1",
            "unit_type": unit_type_fixture.name,
            "active": 1,
        }).insert()

        unit2 = frappe.get_doc({
            "doctype": "Unit",
            "unit_name": "Test Unit 2",
            "unit_type": unit_type_fixture.name,
            "active": 0,
        }).insert()

        # Verify that they have the same unit attributes as the Unit Type
        unit_type_attributes = [attribute.name for attribute in unit_type_fixture.unit_attributes]
        unit1_unit_attributes = [attribute.attribute_link for attribute in unit1.unit_attributes]
        unit2_unit_attributes = [attribute.attribute_link for attribute in unit2.unit_attributes]

        self.assertEqual(unit_type_attributes, unit1_unit_attributes)
        self.assertEqual(unit_type_attributes, unit2_unit_attributes)

        # Make modifications to the Unit Type attributes
        unit_type_fixture.unit_attributes = []
        unit_type_fixture.save()
        unit_type_fixture.reload()
        unit1.reload()
        unit2.reload()

        # Verify that they are propagated
        unit_type_attributes = [attribute.name for attribute in unit_type_fixture.unit_attributes]
        unit1_unit_attributes = [attribute.attribute_link for attribute in unit1.unit_attributes]
        unit2_unit_attributes = [attribute.attribute_link for attribute in unit2.unit_attributes]

        self.assertEqual(unit_type_attributes, unit1_unit_attributes)
        self.assertEqual(unit_type_attributes, unit2_unit_attributes)

        # Need to delete them directly; leaving to tearDown produces errors
        frappe.delete_doc("Unit", unit1.name, delete_permanently=True)
        frappe.delete_doc("Unit", unit2.name, delete_permanently=True)

    # Unit Attribute Testing

    def test_data_attribute_value_cannot_be_multiline(self):
        """Test that the default value for Data attributes cannot be multiline"""

        # Get a fixture
        unit_fixture = self.unitTypes.fixtures.get(self.dt)[0]

        # Add a Data type attribute to it with invalid default_value

        attribute_item = frappe._dict(
            doctype="Unit Type Attribute Item",
            title="Test Attribute 1",
            attribute_type="Data",
            select_options="",
            default_value="1\n2"
        )

        unit_fixture.unit_attributes = [
            frappe.get_doc(attribute_item)
        ]

        # Verify it fails
        with self.assertRaises(UnitAttributeError):
            unit_fixture.save()

    def test_number_attribute_value_cannot_be_multiline(self):
        """Test that the default value for Number attributes cannot be multiline"""

        # Get a fixture
        unit_fixture = self.unitTypes.fixtures.get(self.dt)[0]

        # Add a Number type attribute to it with a multi-line default_value

        attribute_item = frappe._dict(
            doctype="Unit Type Attribute Item",
            title="Test Attribute 1",
            attribute_type="Number",
            select_options="",
            default_value="1\n2"
        )

        unit_fixture.unit_attributes = [
            frappe.get_doc(attribute_item)
        ]

        # Verify it fails
        with self.assertRaises(UnitAttributeError):
            unit_fixture.save()

    def test_number_attribute_value_cannot_be_non_numeric(self):
        """Test that the default value for Number attributes cannot be non-numeric"""

        # Get a fixture
        unit_fixture = self.unitTypes.fixtures.get(self.dt)[0]

        # Add a Number type attribute to it with a multi-line default_value

        attribute_item = frappe._dict(
            doctype="Unit Type Attribute Item",
            title="Test Attribute 1",
            attribute_type="Number",
            select_options="",
            default_value="non"
        )

        unit_fixture.unit_attributes = [
            frappe.get_doc(attribute_item)
        ]

        # Verify it fails
        with self.assertRaises(UnitAttributeError):
            unit_fixture.save()

    def test_select_attribute_value_cannot_be_multiline(self):
        """Test that the default value for Select attributes cannot be multiline"""

        # Get a fixture
        unit_fixture = self.unitTypes.fixtures.get(self.dt)[0]

        # Add a Select type attribute to it with a multi-line default_value

        attribute_item = frappe._dict(
            doctype="Unit Type Attribute Item",
            title="Test Attribute 1",
            attribute_type="Select",
            select_options="1\n2",
            default_value="1\n2"
        )

        unit_fixture.unit_attributes = [
            frappe.get_doc(attribute_item)
        ]

        # Verify it fails
        with self.assertRaises(UnitAttributeError):
            unit_fixture.save()

    def test_select_attribute_value_cannot_be_a_value_not_in_options(self):
        """
        Test that the default value for Select attributes cannot be
        a value that does not exist in the options
        """

        # Get a fixture
        unit_fixture = self.unitTypes.fixtures.get(self.dt)[0]

        # Add a Select type attribute to it with a multi-line default_value

        attribute_item = frappe._dict(
            doctype="Unit Type Attribute Item",
            title="Test Attribute 1",
            attribute_type="Select",
            select_options="1\n2",
            default_value="non"
        )

        unit_fixture.unit_attributes = [
            frappe.get_doc(attribute_item)
        ]

        # Verify it fails
        with self.assertRaises(UnitAttributeError):
            unit_fixture.save()

    def test_multiselect_attribute_value_cannot_be_a_value_not_in_options(self):
        """
        Test that the default value for Multi-Select attributes
        cannot be a value that does not exist in the options
        """

        # Get a fixture
        unit_fixture = self.unitTypes.fixtures.get(self.dt)[0]

        # Add a Select type attribute to it with a default_value that does not exist in the options

        attribute_item = frappe._dict(
            doctype="Unit Type Attribute Item",
            title="Test Attribute 1",
            attribute_type="Select",
            select_options="1\n2",
            default_value="3"
        )

        unit_fixture.unit_attributes = [
            frappe.get_doc(attribute_item)
        ]

        # Verify it fails
        with self.assertRaises(UnitAttributeError):
            unit_fixture.save()

    def test_select_attribute_needs_options(self):
        """Test that if an attribute is of the type Select it needs options"""

        unit_type = frappe.get_doc(frappe._dict(
            doctype=self.dt,
            title="Test UnitType infinity",
            unit_attributes=[
                frappe._dict(
                    title="Test Attribute 1",
                    attribute_type="Select",
                    default_value="Option 1"
                )
            ]
        ))

        # Select with no options should fail
        with self.assertRaises(UnitAttributeError):
            unit_type.insert()

    def test_select_attribute_needs_unique_options(self):
        """Test that if an attribute is of the type Select options must be unique"""

        unit_type = frappe.get_doc(frappe._dict(
            doctype=self.dt,
            title="Test UnitType infinity",
            unit_attributes=[
                frappe._dict(
                    title="Test Attribute 1",
                    attribute_type="Select",
                    default_value="Option 1\nOption 1"
                )
            ]
        ))

        # Select with non-unique options should fail
        with self.assertRaises(UnitAttributeError):
            unit_type.insert()

    def test_multiselect_attribute_needs_options(self):
        """Test that if an attribute is of the type Multi-Select it needs options"""

        unit_type = frappe.get_doc(frappe._dict(
            doctype=self.dt,
            title="Test UnitType infinity",
            unit_attributes=[
                frappe._dict(
                    title="Test Attribute 1",
                    attribute_type="Multi-Select",
                    default_value="Option 1"
                )
            ]
        ))

        # Multi-Select with no options should fail
        with self.assertRaises(UnitAttributeError):
            unit_type.insert()

    def test_multiselect_attribute_needs_unique_options(self):
        """Test that if an attribute is of the type Multi-Select options must be unique"""

        unit_type = frappe.get_doc(frappe._dict(
            doctype=self.dt,
            title="Test UnitType infinity",
            unit_attributes=[
                frappe._dict(
                    title="Test Attribute 1",
                    attribute_type="Multi-Select",
                    default_value="Option 1\nOption 1"
                )
            ]
        ))

        # Multi-Select with non unique options should fail
        with self.assertRaises(UnitAttributeError):
            unit_type.insert()
