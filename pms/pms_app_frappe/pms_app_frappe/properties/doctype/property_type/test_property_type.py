# Copyright (c) 2022, Leam Technology Systems and Contributors
# See license.txt

import unittest

import frappe
from frappe_testing.test_fixture import TestFixture
from pms_app.properties.doctype.unit_type.test_unit_type import UnitTypeFixtures
from pms_app.properties.exceptions import UnitError, UnitTypeNotFound


class PropertyTypeFixtures(TestFixture):

    def __init__(self):
        super().__init__()
        self.DEFAULT_DOCTYPE = "Property Type"
        self.dependent_fixtures = [
            UnitTypeFixtures
        ]

    def make_fixtures(self):

        fixture1 = frappe.get_doc(frappe._dict(
            doctype="Property Type",
            title="Test Property Type1",
            has_units=1,
            unit_types=[
                frappe.get_doc(
                    doctype="Unit Type Item",
                    enabled=1,
                    unit_type=self.get_dependencies("Unit Type")[0].name
                ),
                frappe.get_doc(
                    doctype="Unit Type Item",
                    enabled=1,
                    unit_type=self.get_dependencies("Unit Type")[1].name
                )
            ]
        )).insert()
        self.add_document(fixture1)

        fixture2 = frappe.get_doc(frappe._dict(
            doctype="Property Type",
            title="Test Property Type2",
            has_units=1,
            unit_types=[
                frappe.get_doc(
                    doctype="Unit Type Item",
                    enabled=1,
                    unit_type=self.get_dependencies("Unit Type")[0].name
                )
            ]
        )).insert()
        self.add_document(fixture2)


class TestPropertyType(unittest.TestCase):

    dt = "Property Type"
    propertyTypes = PropertyTypeFixtures()

    def setUp(self) -> None:
        self.propertyTypes.setUp()

    def tearDown(self) -> None:
        self.propertyTypes.tearDown()

    def test_cannot_save_without_unit_types_if_has_units_is_selected(self):
        """Test that at least one Unit Type is needed if has_units is selected"""

        # Get a Property Type fixture
        property_type_fixture = self.propertyTypes.fixtures.get(self.dt)[1]

        # Sanity check: Make sure has_units is selected
        self.assertEqual(property_type_fixture.has_units, 1)

        # Verify that has_units needs at least one Unit
        property_type_fixture.unit_types = []
        with self.assertRaises(UnitError):
            property_type_fixture.save()

    def test_unit_types_removed_if_has_units_is_deselected(self):
        """
        Test that all Unit Types are removed from a Property Type if has_units is not deselected
        """

        # Get a Property Type fixture
        property_type_fixture = self.propertyTypes.fixtures.get(self.dt)[1]

        # Check that it has some unit_types
        self.assertTrue(property_type_fixture.unit_types)

        # Check that if has_units is deselected, existing Unit Types are removed
        property_type_fixture.has_units = 0
        property_type_fixture.save()
        property_type_fixture.reload()
        self.assertEqual(len(property_type_fixture.unit_types), 0)

    def test_cannot_add_unit_types_if_has_units_is_not_selected(self):
        """
        Test that a Property Type cannot add a Unit Type if has_units is not selected
        """

        # Get a Property Type fixture
        property_type_fixture = self.propertyTypes.fixtures.get(self.dt)[1]

        # Deselect has_units
        property_type_fixture.has_units = 0
        property_type_fixture.save()
        property_type_fixture.reload()

        # Check that adding Unit Types does not work

        property_type_fixture.unit_types.append(
            frappe.get_doc(frappe._dict(
                doctype="Unit Type Item",
                parenttype=property_type_fixture.doctype,
                parent=property_type_fixture.name,
                parentfield="unit_types",
                enabled=1,
                unit_type=self.propertyTypes.get_dependencies("Unit Type")[1].name
            ))
        )

        property_type_fixture.save()
        property_type_fixture.reload()

        self.assertEqual(len(property_type_fixture.unit_types), 0)

    def test_only_enabled_unit_types_allowed(self):
        """Test that only enabled Units Types can be added to a Property Type"""

        # Get a Unit Type, disable it
        unit_type_fixture = self.propertyTypes.get_dependencies("Unit Type")[0]
        unit_type_fixture.enabled = 0
        unit_type_fixture.save()

        # Try to add it to Property Type

        property_type_fixture = self.propertyTypes.fixtures.get(self.dt)[0]

        property_type_fixture.unit_type = [
            frappe.get_doc(frappe._dict(
                doctype="Unit Type Item",
                unit_type=unit_type_fixture.name
            ))
        ]

        # Verify it fails
        with self.assertRaises(UnitTypeNotFound):
            property_type_fixture.save()

    def test_property_type_set_disabled_propagates_to_properties(self):
        """Test that if a Property Type is disabled, all linked Properties are disabled also"""

        # Get a Property Type, enabled
        property_type_fixture = self.propertyTypes.fixtures.get(self.dt)[0]

        # Make at least two Properties with the Property Type, both active

        beneficiary_fixture = frappe.get_doc(frappe._dict(
            doctype="PMS Contact",
            first_name="Test beneficiary"
        )).insert()
        self.propertyTypes.add_document(beneficiary_fixture)

        property_fix_1 = frappe.get_doc(frappe._dict(
            doctype="Property",
            property_name="Test Property infinity",
            property_type=property_type_fixture.name,
            beneficiary=beneficiary_fixture.name,
        )).insert()
        self.propertyTypes.add_document(property_fix_1)

        property_fix_2 = frappe.get_doc(frappe._dict(
            doctype="Property",
            property_name="Test Property infinity+1",
            property_type=property_type_fixture.name,
            beneficiary=beneficiary_fixture.name,
        )).insert()
        self.propertyTypes.add_document(property_fix_2)

        # Sanity check...
        self.assertEqual(property_type_fixture.enabled, 1)
        self.assertEqual(property_fix_1.active, 1)
        self.assertEqual(property_fix_2.active, 1)

        # Disable the Property, verify that the Properties are deactivated

        property_type_fixture.enabled = 0
        property_type_fixture.save()

        property_type_fixture.reload()
        property_fix_1.reload()
        property_fix_2.reload()

        self.assertEqual(property_type_fixture.enabled, 0)
        self.assertEqual(property_fix_1.active, 0)
        self.assertEqual(property_fix_2.active, 0)

        # Re-enable the Property Type and confirm that Properties are still deactivated

        property_type_fixture.enabled = 1
        property_type_fixture.save()

        property_type_fixture.reload()
        property_fix_1.reload()
        property_fix_2.reload()

        self.assertEqual(property_type_fixture.enabled, 1)
        self.assertEqual(property_fix_1.active, 0)
        self.assertEqual(property_fix_2.active, 0)

    def test_property_types_unit_type_changes_propagate_to_properties(self):
        """
        Tests that if Unit Types are removed or changed on a Property Type,
        the linked Properties also update
        """

        # Get a Property Type, with at least two Unit Types
        fixture = self.propertyTypes.fixtures.get(self.dt)[0]
        unit_type_1 = fixture.unit_types[0].unit_type
        unit_type_2 = fixture.unit_types[1].unit_type

        # Link it to a Property, with Units of same Unit Types

        beneficiary_fixture = frappe.get_doc(frappe._dict(
            doctype="PMS Contact",
            first_name="Test beneficiary"
        )).insert()
        self.propertyTypes.add_document(beneficiary_fixture)

        unit_fix_1 = frappe.get_doc(frappe._dict(
            doctype="Unit",
            unit_name="Test Unit infinity",
            unit_type=unit_type_1
        )).insert()
        self.propertyTypes.add_document(unit_fix_1)

        unit_fix_2 = frappe.get_doc(frappe._dict(
            doctype="Unit",
            unit_name="Test Unit infinity +1",
            unit_type=unit_type_2
        )).insert()
        self.propertyTypes.add_document(unit_fix_2)

        property_fix = frappe.get_doc(frappe._dict(
            doctype="Property",
            property_name="Test Property",
            property_type=fixture.name,
            beneficiary=beneficiary_fixture.name,
            units=[
                frappe.get_doc(frappe._dict(
                    doctype="Unit Item",
                    unit=unit_fix_1.name
                )),
                frappe.get_doc(frappe._dict(
                    doctype="Unit Item",
                    unit=unit_fix_2.name
                )),
            ]
        )).insert()
        self.propertyTypes.add_document(property_fix)

        property_fix_unit_types = [unit.unit_type for unit in property_fix.units]
        self.assertIn(unit_type_1, property_fix_unit_types)
        self.assertIn(unit_type_2, property_fix_unit_types)

        # Remove a Unit Type, verify Property updates

        fixture.update({"unit_types": [fixture.unit_types[0]]})
        fixture.save()

        property_fix.reload()
        property_fix_unit_types = [unit.unit_type for unit in property_fix.units]
        self.assertIn(unit_type_1, property_fix_unit_types)
        self.assertNotIn(unit_type_2, property_fix_unit_types)

        # Change a Unit Type, verify Property updates

        unit_type_item = fixture.unit_types[0].update({"enabled": 0})
        fixture.update({"unit_types": [unit_type_item]})
        fixture.save()

        property_fix.reload()
        property_fix_unit_types = [unit.unit_type for unit in property_fix.units]
        self.assertNotIn(unit_type_1, property_fix_unit_types)
