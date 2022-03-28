from unittest import TestCase
from asyncer import runnify

import renovation
from renovation.tests import RenovationTestFixture

from pms_app.pms_core.models.event_log.event_log import EventLog
from pms_app.pms_core.models.pms_contact.test_pms_contact import PMSContactFixtures, PMSContact
from .pms_custom_field import (
    PMSCustomField,
    CF_FIELDNAME_PREFIX,
    PMS_CUSTOMIZABLE_ENTITY_TYPES_HOOK)
from .exceptions import DuplicateFieldname, InvalidCustomFieldOption, NonCustomizableEntityType


class PMSCustomFieldTestFixture(RenovationTestFixture):

    def __init__(self):
        super().__init__()
        self.DEFAULT_MODEL = PMSCustomField
        self.dependent_fixtures = [PMSContactFixtures]

        self.TEST_ENTITY = None
        self.TEST_ENTITY_TYPE = PMSContact.get_doctype()
        self.NON_EXCLUDED_ENTITY = EventLog.get_doctype()

    async def make_fixtures(self):

        self.add_document(await PMSCustomField(dict(
            label="Gamer Tag",
            fieldtype="Data",
            description="###",
            entity_type=None,  # General to all!
        )).insert())

        self.add_document(await PMSCustomField(dict(
            label="Height X",
            fieldtype="Float",
            description="Height in Ft",
            entity_type=None,  # General to all!
        )).insert())

        self.add_document(await PMSCustomField(dict(
            label="Weight X",
            fieldtype="Float",
            description="Weight in Ft",
            entity_type=self.TEST_ENTITY_TYPE,
        )).insert())

        self.add_document(await PMSCustomField(dict(
            label="Color X",
            fieldtype="Select",
            options="RED\nGreen\nBlue\nOrange",
            entities_excluded=[dict(model=self.TEST_ENTITY_TYPE)]  # on all except PMS Contact
        )).insert())

        self.TEST_ENTITY = self.get_dependencies(PMSContact)[0].name
        self.add_document(await PMSCustomField(dict(
            label="Net Worth",
            fieldtype="Integer",
            entity_type=self.TEST_ENTITY_TYPE,
            entity=self.TEST_ENTITY
        )).insert())


class TestPMSCustomField(TestCase):
    custom_fields = PMSCustomFieldTestFixture()

    @runnify
    async def setUp(self) -> None:
        await self.custom_fields.setUp()

    @runnify
    async def tearDown(self) -> None:
        await self.custom_fields.tearDown()

    @runnify
    async def test_fieldname(self):
        label = "Test ABC"
        r = PMSCustomField(dict(
            label=label,
            fieldtype="Data",
        ))
        await r.insert()
        self.custom_fields.add_document(r)

        self.assertEqual(r.fieldname, CF_FIELDNAME_PREFIX + renovation.scrub(label))

    @runnify
    async def test_customizable_entity_type(self):
        r = PMSCustomField(dict(
            label="Test A",
            fieldtype="Data",
            entity_type="User"
        ))

        with self.assertRaises(NonCustomizableEntityType):
            await r.insert()

    @runnify
    async def test_unique_fieldname(self):
        r = PMSCustomField(dict(
            label=self.custom_fields[0].label,
            fieldtype="Data",
            entity_type="PMS Contact"
        ))

        with self.assertRaises(DuplicateFieldname):
            await r.save()

    @runnify
    async def test_data_field(self):
        r = PMSCustomField(dict(
            label="Test A",
            fieldtype="Data",
            options="Random"
        ))

        with self.assertRaises(InvalidCustomFieldOption):
            await r.insert()

        r = PMSCustomField(dict(
            label="Test AX",
            fieldtype="Data",
            options="Email"  # proper
        ))

        await r.insert()
        self.custom_fields.add_document(r)

        r = PMSCustomField(dict(
            label="Test AB",
            fieldtype="Data",
            options=None  # Empty
        ))

        await r.insert()
        self.custom_fields.add_document(r)

    @runnify
    async def test_select_field(self):
        r = PMSCustomField(dict(
            label="Test AX",
            fieldtype="Select",
            options=None
        ))

        with self.assertRaises(InvalidCustomFieldOption):
            await r.insert()

        r = PMSCustomField(dict(
            label="Test BX",
            fieldtype="Select",
            options="AB\nCD"  # Normal
        ))

        await r.insert()
        self.custom_fields.add_document(r)

        r = PMSCustomField(dict(
            label="Test CX",
            fieldtype="Select",
            options="AB  \n  CD  "
        ))

        await r.insert()
        self.custom_fields.add_document(r)

        self.assertEqual(r.options, "AB\nCD")

    @runnify
    async def test_options_on_int_and_float(self):
        r = PMSCustomField(dict(
            label="Test AX",
            fieldtype="Integer",
            options="Email"
        ))

        with self.assertRaises(InvalidCustomFieldOption):
            await r.insert()

        r = PMSCustomField(dict(
            label="Test BX",
            fieldtype="Float",
            options="Random"
        ))

        with self.assertRaises(InvalidCustomFieldOption):
            await r.insert()

        # Proper
        r = PMSCustomField(dict(
            label="Test CX",
            fieldtype="Float",
            options=None
        ))

        await r.insert()
        self.custom_fields.add_document(r)

        r = PMSCustomField(dict(
            label="Test DX",
            fieldtype="Integer",
            options=None
        ))

        await r.insert()
        self.custom_fields.add_document(r)

    @runnify
    async def test_rename_label(self):
        r = PMSCustomField(dict(
            label="Test A",
            fieldtype="Data",
            options="Email"  # proper
        ))

        await r.insert()
        self.custom_fields.add_document(r)
        fieldname = r.fieldname

        r.label = "Test B"
        await r.save()

        self.assertEqual(fieldname, r.fieldname)

    @runnify
    async def test_fieldtype_updates(self):
        r = PMSCustomField(dict(
            label="Test A",
            fieldtype="Data",
            options="Email"  # proper
        ))

        await r.insert()
        self.custom_fields.add_document(r)

        # Change to Select
        r.fieldtype = "Select"
        await r.save()
        self.assertEqual(r.fieldtype, "Select")

        # Change to Integer
        r.fieldtype = "Integer"
        with self.assertRaises(InvalidCustomFieldOption):
            await r.save()

        await r.reload()
        r.options = None
        r.fieldtype = "Integer"

        await r.save()
        self.assertEqual(r.fieldtype, "Integer")

    @runnify
    async def test_get_applicable_entity_types(self):
        r = PMSCustomField(dict(
            label="Test A",
            fieldtype="Data",
            entity_type="PMS Contact"
        ))
        await r.insert()
        self.custom_fields.add_document(r)

        self.assertListEqual(r.get_applicable_entity_types(), ["PMS Contact"])

        r.entity_type = None
        await r.save()

        _hook = renovation.get_hooks(PMS_CUSTOMIZABLE_ENTITY_TYPES_HOOK)
        self.assertGreater(len(_hook), 1)
        self.assertCountEqual(r.get_applicable_entity_types(), list(set(_hook)))

        r.append("entities_excluded", dict(model=_hook[0]))
        await r.save()

        _hook.remove(_hook[0])
        self.assertCountEqual(r.get_applicable_entity_types(), list(set(_hook)))
