from unittest import TestCase
from asyncer import runnify
from pms_app.pms_core.models.event_log.event_log import EventLog

from renovation.tests import RenovationTestFixture
from pms_app.pms_core.models.pms_contact.test_pms_contact import PMSContactFixtures, PMSContact
from .pms_custom_field import PMSCustomField


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
