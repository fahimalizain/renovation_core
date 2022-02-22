# Copyright (c) 2022, Leam Technology Systems and Contributors
# See license.txt

import unittest

import frappe
from frappe_testing.test_fixture import TestFixture
from pms_app.properties.doctype.property_type.test_property_type import PropertyTypeFixtures
from pms_app.pms_core.doctype.pms_contact.test_pms_contact import PMSContactFixtures
from pms_app.properties.doctype.unit.test_unit import UnitFixtures
from pms_app.properties.exceptions import PropertyTypeNotEnabled, UnitError, UnitItemError


class PropertyFixtures(TestFixture):

    def __init__(self):
        super().__init__()
        self.DEFAULT_DOCTYPE = "Property"
        self.dependent_fixtures = [
            PropertyTypeFixtures,
            PMSContactFixtures,
            UnitFixtures
        ]

    def make_fixtures(self):

        fix1 = frappe.get_doc(frappe._dict(
            doctype=self.DEFAULT_DOCTYPE,
            property_name="Test Property 1",
            property_type=self.get_dependencies("Property Type")[0].name,
            beneficiary=self.get_dependencies("PMS Contact")[0].name,
        )).insert()
        self.add_document(fix1)

        fix2 = frappe.get_doc(frappe._dict(
            doctype=self.DEFAULT_DOCTYPE,
            property_name="Test Property 2",
            property_type=self.get_dependencies("Property Type")[0].name,
            beneficiary=self.get_dependencies("PMS Contact")[0].name,
        )).insert()
        self.add_document(fix2)

        fix3 = frappe.get_doc(frappe._dict(
            doctype=self.DEFAULT_DOCTYPE,
            property_name="Test Property 3",
            property_type=self.get_dependencies("Property Type")[1].name,
            beneficiary=self.get_dependencies("PMS Contact")[0].name,
        )).insert()
        self.add_document(fix3)


class TestProperty(unittest.TestCase):

    dt = "Property"
    properties = PropertyFixtures()

    def setUp(self) -> None:
        self.properties.setUp()

    def tearDown(self) -> None:
        self.properties.tearDown()

    def test_cannot_link_property_to_a_disabled_property_type(self):
        """Test that a Property cannot be linked to a disabled Property Type"""

        # Get a Property Type
        property_fixture = self.properties.get_dependencies("Property Type")[1]

        # Disable it
        property_fixture.enabled = 0
        property_fixture.save()

        # Try to create a Property with the Property Type

        beneficiary_fixture = self.properties.get_dependencies("PMS Contact")[0]

        property_doc = frappe.get_doc(frappe._dict(
            doctype="Property",
            property_name="Test Property infinity",
            property_type=property_fixture.name,
            beneficiary=beneficiary_fixture.name,
        ))

        # Verify it fails
        with self.assertRaises(PropertyTypeNotEnabled):
            property_doc.insert()

    def test_unique_units_only(self):
        """Test that cannot add a Unit if it is already added to another Property"""

        # Get a Property and add a Unit to it

        property_fixture_1 = self.properties.fixtures.get("Property")[0]

        unit_fixture = self.properties.get_dependencies("Unit")[0]

        property_fixture_1.units = [
            frappe.get_doc(frappe._dict(
                doctype="Unit Item",
                parenttype=property_fixture_1.doctype,
                parent=property_fixture_1.name,
                parentfield="units",
                unit=unit_fixture.name
            ))
        ]

        property_fixture_1.update_children()
        property_fixture_1.reload()

        # Get another Property and try to add the same Unit to it

        property_fixture_2 = self.properties.fixtures.get("Property")[1]

        property_fixture_2.units = [
            frappe.get_doc(frappe._dict(
                doctype="Unit Item",
                unit=unit_fixture.name
            ))
        ]

        # Verify that it fails
        with self.assertRaises(UnitError):
            property_fixture_2.save()

    def test_cannot_add_units_to_property_with_incompatible_unit_types(self):
        """Validate that only Units with Unit Type existing on the Property Type can be added"""

        # Get a Property
        fixture = self.properties.fixtures.get(self.dt)[2]

        # Get a Unit that is not of the type that are on the linked Property Type
        unit_fixture = self.properties.get_dependencies("Unit")[2]

        # Try to add the Units to the Property
        fixture.update({"units": [
            frappe.get_doc(frappe._dict(
                doctype="Unit Item",
                parenttype=fixture.doctype,
                parent=fixture.name,
                parentfield="units",
                unit=unit_fixture.name
            ))
        ]})

        # Verify that it fails
        with self.assertRaises(UnitItemError):
            fixture.save()
