from unittest import TestCase
from asyncer import runnify

import renovation
from renovation.tests import RenovationTestFixture

from pms_app.pms_core.models.event_log.event_log import EventLog
from pms_app.pms_core.models.pms_contact.test_pms_contact import PMSContactFixtures, PMSContact
from .pms_custom_field import PMSCustomField
from .exceptions import InvalidCustomFieldOption


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

        self.assertEqual(r.fieldname, renovation.scrub(label))

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
            label="Test A",
            fieldtype="Data",
            options="Email"  # proper
        ))

        await r.insert()
        self.custom_fields.add_document(r)

        r = PMSCustomField(dict(
            label="Test A",
            fieldtype="Data",
            options=None  # Empty
        ))

        await r.insert()
        self.custom_fields.add_document(r)

    @runnify
    async def test_select_field(self):
        r = PMSCustomField(dict(
            label="Test A",
            fieldtype="Select",
            options=None
        ))

        with self.assertRaises(InvalidCustomFieldOption):
            await r.insert()

        r = PMSCustomField(dict(
            label="Test A",
            fieldtype="Select",
            options="AB\nCD"  # Normal
        ))

        await r.insert()
        self.custom_fields.add_document(r)

        r = PMSCustomField(dict(
            label="Test A",
            fieldtype="Select",
            options="AB  \n  CD  "
        ))

        await r.insert()
        self.custom_fields.add_document(r)

        self.assertEqual(r.options, "AB\nCD")
