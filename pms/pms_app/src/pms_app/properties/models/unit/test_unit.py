# Copyright (c) 2021, Leam Technology Systems and Contributors
# See license.txt

import unittest
from asyncer import runnify

import renovation
from renovation.tests import RenovationTestFixture
from pms_app.pms_core.models.pms_contact.pms_contact import PMSContact
from pms_app.properties.models.property.property import Property
from pms_app.properties.models.property_type.property_type import PropertyType
from pms_app.properties.models.unit_type.test_unit_type import UnitTypeFixtures, UnitType
from pms_app.properties.models.unit_attribute_item.unit_attribute_item import UnitAttributeItem
from pms_app.properties.models.unit_item.unit_item import UnitItem
from pms_app.properties.models.unit_type_item.unit_type_item import UnitTypeItem
from pms_app.properties.exceptions import UnitAttributeError, UnitTypeNotFound
from .unit import Unit


class UnitFixtures(RenovationTestFixture):

    def __init__(self):
        super().__init__()
        self.DEFAULT_MODEL = Unit
        self.dependent_fixtures = [
            UnitTypeFixtures
        ]

    async def make_fixtures(self):

        fix1 = Unit(renovation._dict(
            unit_name="Test Unit 1",
            unit_type=self.get_dependencies(UnitType)[0].name
        ))
        await fix1.insert()
        self.add_document(fix1)

        fix2 = Unit(renovation._dict(
            unit_name="Test Unit 2",
            unit_type=self.get_dependencies(UnitType)[0].name
        ))
        await fix2.insert()
        self.add_document(fix2)

        fix3 = Unit(renovation._dict(
            unit_name="Test Unit 3",
            active=0,
            unit_type=self.get_dependencies(UnitType)[1].name
        ))
        await fix3.insert()
        self.add_document(fix3)


class TestUnit(unittest.TestCase):

    dt = Unit
    units = UnitFixtures()

    @runnify
    async def setUp(self) -> None:
        await self.units.setUp()

    @runnify
    async def tearDown(self) -> None:
        await self.units.tearDown()

    @runnify
    async def test_active_unit_cannot_be_linked_to_disabled_unit_type(self):
        """Test that only enabled Unit Types can be linked to a Unit"""

        # Get a disabled Unit Type
        type_fixture = self.units.get_dependencies(UnitType)[1]
        type_fixture.enabled = 0
        await type_fixture.save()
        await type_fixture.reload()

        # Try to save it to an Active Unit
        with self.assertRaises(UnitTypeNotFound):
            await Unit(renovation._dict(
                unit_name="Test Unit 4",
                active=1,
                unit_type=type_fixture.name
            )).insert()

    @runnify
    async def test_deactivated_unit_cannot_be_linked_to_disabled_unit_type(self):
        """Test that disabled Unit Types can be linked to a deactivated Unit"""

        # Get a disabled Unit Type
        type_fixture = self.units.get_dependencies(UnitType)[1]
        type_fixture.enabled = 0
        await type_fixture.save()
        await type_fixture.reload()

        # Try to save it on an deactivated one
        unit = Unit(renovation._dict(
            unit_name="Test Unit infinity",
            active=0,
            unit_type=type_fixture.name
        ))
        await unit.insert()
        self.units.add_document(unit)

    @runnify
    async def test_copy_unit_type_attributes_on_insert(self):
        """Test that on insert, attributes are auto-copied from the linked Unit Type"""

        # Get a Unit fixture
        unit_fixture = self.units.fixtures.get(Unit)[0]

        # Verify that the attributes have been copied over from the Unit Type

        unit_type_fixture = await UnitType.get_doc(unit_fixture.unit_type)

        self.assertEqual(len(unit_type_fixture.unit_attributes), len(unit_fixture.unit_attributes))

        unit_type_fixture.unit_attributes.sort(key=unit_attributes_sort_key)
        unit_fixture.unit_attributes.sort(key=unit_attributes_sort_key)

        for type_attribute, unit_attribute in \
                zip(unit_type_fixture.unit_attributes, unit_fixture.unit_attributes):
            self.assertEqual(type_attribute.name, unit_attribute.attribute_link)
            self.assertEqual(type_attribute.title, unit_attribute.title)
            self.assertEqual(type_attribute.attribute_type, unit_attribute.attribute_type)
            self.assertEqual(type_attribute.select_options, unit_attribute.select_options)
            self.assertEqual(type_attribute.default_value, unit_attribute.value)

    @runnify
    async def test_copy_unit_type_attributes_on_save(self):
        """Test that on save, attributes are auto-copied from the linked Unit Type"""

        # Get a Unit fixture
        unit_fixture = self.units.fixtures.get(Unit)[0]

        # Change its Unit Type to something different

        unit_type_fixture = self.units.get_dependencies(UnitType)[1]
        unit_type_fixture.enabled = 1
        await unit_type_fixture.save()

        self.assertNotEqual(unit_fixture.unit_type, unit_type_fixture.name)

        unit_fixture.unit_type = unit_type_fixture.name
        await unit_fixture.save()
        await unit_fixture.reload()

        # Verify that the attributes have been copied over from the new Unit Type

        unit_type_fixture.unit_attributes.sort(key=unit_attributes_sort_key)
        unit_fixture.unit_attributes.sort(key=unit_attributes_sort_key)

        for type_attribute, unit_attribute in \
                zip(unit_type_fixture.unit_attributes, unit_fixture.unit_attributes):
            self.assertEqual(type_attribute.name, unit_attribute.attribute_link)
            self.assertEqual(type_attribute.title, unit_attribute.title)
            self.assertEqual(type_attribute.attribute_type, unit_attribute.attribute_type)
            self.assertEqual(type_attribute.select_options, unit_attribute.select_options)
            self.assertEqual(type_attribute.default_value, unit_attribute.value)

    # Unit Attribute Tests
    @runnify
    async def test_only_linked_unit_type_attributes_can_be_added_to_unit(self):
        """Test that only Unit Attributes that exist on the linked Unit Type can be added"""

        # Get a fixture
        unit_fixture = self.units.fixtures.get(self.dt)[0]

        # Try to append a Unit Attribute on it that is not on the linked Unit Type

        invalid_attribute = (await UnitAttributeItem.get_all(
            filters=[["parent", "!=", unit_fixture.unit_type]]
        ))[0].name

        invalid_attribute = await UnitAttributeItem.get_doc(invalid_attribute)

        unit_fixture.unit_attributes.append(invalid_attribute)
        await unit_fixture.save()
        await unit_fixture.reload()

        # Verify that it is not saved
        self.assertNotIn(invalid_attribute, unit_fixture.unit_attributes)

    @runnify
    async def test_data_attribute_value_cannot_be_multiline(self):
        """Test that the value for Data attributes cannot be multiline"""

        # Get a unit
        unit = self.units.fixtures.get(self.dt)[0]

        # Verify it has an attribute of the Data type
        fixture_types = [attribute.attribute_type for attribute in unit.unit_attributes]
        self.assertIn("Data", fixture_types)

        attributes = unit.unit_attributes

        # Try to set an invalid value on the Data attribute
        for attribute in attributes:
            if attribute.attribute_type == "Data":

                test_attribute = UnitAttributeItem(renovation._dict(
                    attribute_link=attribute.attribute_link,
                    value="This is the test\nThis is the point of failure"
                ))

                unit.unit_attributes = [test_attribute]

                # Verify it fails if value is multiline
                with self.assertRaises(UnitAttributeError):
                    await unit.save()

    @runnify
    async def test_number_attribute_value_cannot_be_multiline(self):
        """Test that the value for Number attributes cannot be multiline"""

        # Get a unit
        unit = self.units.fixtures.get(self.dt)[0]

        # Verify it has an attribute of the Number type
        fixture_types = [attribute.attribute_type for attribute in unit.unit_attributes]
        self.assertIn("Number", fixture_types)

        attributes = unit.unit_attributes

        # Try to set an invalid value on the Number attribute
        for attribute in attributes:
            if attribute.attribute_type == "Number":

                test_attribute = UnitAttributeItem(renovation._dict(
                    attribute_link=attribute.attribute_link,
                    value="1\n2"
                ))

                unit.unit_attributes = [test_attribute]

                # Verify it fails if value is multiline
                with self.assertRaises(UnitAttributeError):
                    await unit.save()

    @runnify
    async def test_number_attribute_value_cannot_be_non_numeric(self):
        """Test that the value for Number attributes cannot be non-numeric"""

        # Get a unit
        unit = self.units.fixtures.get(self.dt)[0]

        # Verify it has an attribute of the Number type
        fixture_types = [attribute.attribute_type for attribute in unit.unit_attributes]
        self.assertIn("Number", fixture_types)

        attributes = unit.unit_attributes

        # Try to set an invalid value on the Number attribute
        for attribute in attributes:
            if attribute.attribute_type == "Number":

                test_attribute = UnitAttributeItem(renovation._dict(
                    attribute_link=attribute.attribute_link,
                    value="non-numeric"
                ))

                unit.unit_attributes = [test_attribute]

                # Verify it fails if value is multiline
                with self.assertRaises(UnitAttributeError):
                    await unit.save()

    @runnify
    async def test_select_attribute_value_cannot_be_multiline(self):
        """Test that the value for Select attributes cannot be multiline"""

        # Get a unit
        unit = self.units.fixtures.get(self.dt)[0]

        # Verify it has an attribute of the Select type
        fixture_types = [attribute.attribute_type for attribute in unit.unit_attributes]
        self.assertIn("Select", fixture_types)

        attributes = unit.unit_attributes

        # Try to set an invalid value on the Select attribute
        for attribute in attributes:
            if attribute.attribute_type == "Select":

                test_attribute = UnitAttributeItem(renovation._dict(
                    attribute_link=attribute.attribute_link,
                    value="This is the test\nThis is the point of failure"
                ))

                unit.unit_attributes = [test_attribute]

                # Verify it fails if value is multiline
                with self.assertRaises(UnitAttributeError):
                    await unit.save()

    @runnify
    async def test_select_attribute_value_cannot_be_a_value_not_in_options(self):
        """
        Test that the value for Select attributes cannot be a value that is not specified in options
        """

        # Get a unit
        unit = self.units.fixtures.get(self.dt)[0]

        # Verify it has an attribute of the Select type
        fixture_types = [attribute.attribute_type for attribute in unit.unit_attributes]
        self.assertIn("Select", fixture_types)

        attributes = unit.unit_attributes

        # Try to set an invalid value on the Select attribute
        for attribute in attributes:
            if attribute.attribute_type == "Select":

                test_attribute = UnitAttributeItem(renovation._dict(
                    attribute_link=attribute.attribute_link,
                    value="not in options"
                ))

                unit.unit_attributes = [test_attribute]

                # Verify it fails if value does exist in options
                with self.assertRaises(UnitAttributeError):
                    await unit.save()

    @runnify
    async def test_multiselect_attribute_value_cannot_be_a_value_not_in_options(self):
        """
        Test that the value for Multi-Select attributes cannot be
        a value that is not specified in options
        """

        # Get a unit
        unit = self.units.fixtures.get(self.dt)[0]

        # Verify it has an attribute of the Select type
        fixture_types = [attribute.attribute_type for attribute in unit.unit_attributes]
        self.assertIn("Multi-Select", fixture_types)

        attributes = unit.unit_attributes

        # Try to set an invalid value on the Select attribute
        for attribute in attributes:
            if attribute.attribute_type == "Multi-Select":

                test_attribute = UnitAttributeItem(renovation._dict(
                    attribute_link=attribute.attribute_link,
                    value="not in options"
                ))

                unit.unit_attributes = [test_attribute]

                # Verify it fails if value is not in options
                with self.assertRaises(UnitAttributeError):
                    await unit.save()

    # Linked Property Tests
    @runnify
    async def test_update_unit_type_of_unit_on_a_property(self):
        """
        Test that if the Unit Type of a Unit changes,
        the change is reflected in any Property with the Unit
        """

        # Get two Unit Types
        unit_type_fixtures = self.units.get_dependencies(UnitType)
        unit_type_fixtures[1].enabled = 1
        await unit_type_fixtures[1].save()

        # Get a Unit
        unit_fixture = self.units.fixtures.get(Unit)[0]

        # Make a Property; Property is not a dependant fixture so...
        # Also add a Unit Item to it with the Unit you have

        property_type_fixture = PropertyType(renovation._dict(
            title="Test Property Type",
            has_units=1,
            unit_types=[
                UnitTypeItem(renovation._dict(
                    enabled=1,
                    unit_type=unit_type_fixtures[0].name
                )),
                UnitTypeItem(renovation._dict(
                    enabled=1,
                    unit_type=unit_type_fixtures[1].name
                ))
            ]
        ))
        await property_type_fixture.insert()
        self.units.add_document(property_type_fixture)

        beneficiary_fixture = PMSContact(renovation._dict(
            first_name="Test beneficiary"
        ))
        await beneficiary_fixture.insert()
        self.units.add_document(beneficiary_fixture)

        property_fix = Property(renovation._dict(
            property_name="Test Property infinity",
            property_type=property_type_fixture.name,
            beneficiary=beneficiary_fixture.name,
            units=[
                UnitItem(renovation._dict(
                    unit=unit_fixture.name
                ))]
        ))
        await property_fix.insert()
        self.units.add_document(property_fix)

        # Verify that the Unit Type is correct
        self.assertEqual(property_fix.units[0].unit_type, unit_fixture.unit_type)

        # Update the Unit Type of the Unit
        unit_fixture.unit_type = unit_type_fixtures[1].name
        await unit_fixture.save()
        await unit_fixture.reload()
        await property_fix.reload()

        # Verify that the Unit Type on the Property is updated
        self.assertEqual(property_fix.units[0].unit_type, unit_fixture.unit_type)


def unit_attributes_sort_key(attribute):
    return attribute.title
