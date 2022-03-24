from unittest import TestCase
from asyncer import runnify

from renovation.tests import RenovationTestFixture
from pms_app.pms_core.models.pms_contact.test_pms_contact import PMSContactFixtures, PMSContact
from .pms_custom_field import PMSCustomField


class PMSCustomFieldTestFixture(RenovationTestFixture):
    CUSTOM_PMS_CONTACT: str = None

    def __init__(self):
        super().__init__()
        self.DEFAULT_MODEL = PMSCustomField
        self.dependent_fixtures = [PMSContactFixtures]

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
            entity_type=PMSContact.get_doctype(),
        )).insert())

        self.add_document(await PMSCustomField(dict(
            label="Color X",
            fieldtype="Select",
            options="RED\nGreen\nBlue\nOrange",
            entities_excluded=[dict(model=PMSContact.get_doctype())]  # on all except PMS Contact
        )).insert())

        self.CUSTOM_PMS_CONTACT = self.get_dependencies(PMSContact)[0].name
        self.add_document(await PMSCustomField(dict(
            label="Net Worth",
            fieldtype="Integer",
            entity_type=PMSContact.get_doctype(),
            entity=self.CUSTOM_PMS_CONTACT
        )).insert())


class TestPMSCustomField(TestCase):
    custom_fields = PMSCustomFieldTestFixture()

    @runnify
    async def setUp(self) -> None:
        await self.custom_fields.setUp()

    @runnify
    async def tearDown(self) -> None:
        await self.custom_fields.tearDown()
