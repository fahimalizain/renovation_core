# Copyright (c) 2022, Leam Technology Systems and Contributors
# See license.txt

import unittest
from asyncer import runnify
from pms_app.properties.models.unit_item.unit_item import UnitItem

import renovation
from renovation.tests import RenovationTestFixture
from .property import Property
from pms_app.properties.models.property_type.property_type import PropertyType
from pms_app.properties.models.property_type.test_property_type import PropertyTypeFixtures
from pms_app.pms_core.models.test_pms_contact import PMSContactFixtures, PMSContact
from pms_app.properties.models.unit.test_unit import UnitFixtures, Unit
from pms_app.properties.exceptions import PropertyTypeNotEnabled, UnitError, UnitItemError


class PropertyFixtures(RenovationTestFixture):

    def __init__(self):
        super().__init__()
        self.DEFAULT_MODEL = Property
        self.dependent_fixtures = [
            PropertyTypeFixtures,
            PMSContactFixtures,
            UnitFixtures
        ]

    async def make_fixtures(self):

        fix1 = Property(renovation._dict(
            property_name="Test Property 1",
            property_type=self.get_dependencies(PropertyType)[0].name,
            beneficiary=self.get_dependencies(PMSContact)[0].name,
        ))
        await fix1.insert()
        self.add_document(fix1)

        fix2 = Property(renovation._dict(
            property_name="Test Property 2",
            property_type=self.get_dependencies(PropertyType)[0].name,
            beneficiary=self.get_dependencies(PMSContact)[0].name,
        ))
        await fix2.insert()
        self.add_document(fix2)

        fix3 = Property(renovation._dict(
            property_name="Test Property 3",
            property_type=self.get_dependencies(PropertyType)[1].name,
            beneficiary=self.get_dependencies(PMSContact)[0].name,
        ))
        await fix3.insert()
        self.add_document(fix3)


class TestProperty(unittest.TestCase):

    dt = Property
    properties = PropertyFixtures()

    @runnify
    async def setUp(self) -> None:
        await self.properties.setUp()

    @runnify
    async def tearDown(self) -> None:
        await self.properties.tearDown()

    @runnify
    async def test_cannot_link_property_to_a_disabled_property_type(self):
        """Test that a Property cannot be linked to a disabled Property Type"""

        # Get a Property Type
        property_fixture = self.properties.get_dependencies(PropertyType)[1]

        # Disable it
        property_fixture.enabled = 0
        await property_fixture.save()

        # Try to create a Property with the Property Type

        beneficiary_fixture = self.properties.get_dependencies(PMSContact)[0]

        property_doc = Property(renovation._dict(
            property_name="Test Property infinity",
            property_type=property_fixture.name,
            beneficiary=beneficiary_fixture.name,
        ))

        # Verify it fails
        with self.assertRaises(PropertyTypeNotEnabled):
            await property_doc.insert()

    @runnify
    async def test_unique_units_only(self):
        """Test that cannot add a Unit if it is already added to another Property"""

        # Get a Property and add a Unit to it

        property_fixture_1 = self.properties.fixtures.get(Property)[0]

        unit_fixture = self.properties.get_dependencies(Unit)[0]

        property_fixture_1.units = [
            UnitItem(renovation._dict(
                parenttype=property_fixture_1.doctype,
                parent=property_fixture_1.name,
                parentfield="units",
                unit=unit_fixture.name
            ))
        ]

        property_fixture_1.update_children()
        await property_fixture_1.reload()

        # Get another Property and try to add the same Unit to it

        property_fixture_2 = self.properties.fixtures.get(Property)[1]

        property_fixture_2.units = [
            UnitItem(renovation._dict(
                unit=unit_fixture.name
            ))
        ]

        # Verify that it fails
        with self.assertRaises(UnitError):
            await property_fixture_2.save()

    @runnify
    async def test_cannot_add_units_to_property_with_incompatible_unit_types(self):
        """Validate that only Units with Unit Type existing on the Property Type can be added"""

        # Get a Property
        fixture = self.properties.fixtures.get(self.dt)[2]

        # Get a Unit that is not of the type that are on the linked Property Type
        unit_fixture = self.properties.get_dependencies(Unit)[2]

        # Try to add the Units to the Property
        fixture.update({"units": [
            UnitItem(renovation._dict(
                parenttype=fixture.doctype,
                parent=fixture.name,
                parentfield="units",
                unit=unit_fixture.name
            ))
        ]})

        # Verify that it fails
        with self.assertRaises(UnitItemError):
            await fixture.save()
