import unittest
from asyncer import runnify

import renovation
from renovation.tests import RenovationTestFixture
from .pms_contact import PMSContact


class PMSContactFixtures(RenovationTestFixture):

    def __init__(self):
        super().__init__()
        self.DEFAULT_MODEL = PMSContact

    async def make_fixtures(self):

        fixture1 = PMSContact(renovation._dict(
            first_name="Test beneficiary 1"
        ))
        await fixture1.insert()
        self.add_document(fixture1)


class TestPMSContact(unittest.TestCase):
    pms_contacts: PMSContactFixtures = PMSContactFixtures()

    @runnify
    async def setUp(self):
        await self.pms_contacts.setUp()

    @runnify
    async def tearDown(self) -> None:
        await self.pms_contacts.tearDown()

    @runnify
    async def test_user_is_not_created_when_email_mobile_not_supplied(self):
        contact = PMSContact(dict(
            first_name="Test A"
        ))

        await contact.insert()
        await contact.reload()
        self.pms_contacts.add_document(contact)

        self.assertTrue(await PMSContact.exists(contact.name))
        self.assertIsNone(contact.user)

    @runnify
    async def test_user_is_created_when_email_is_supplied(self):
        contact = PMSContact(dict(
            first_name="Test A",
            last_name="Test B",
            email_id="test@test.com"
        ))

        await contact.insert()
        await contact.reload()
        self.pms_contacts.add_document(contact)

        self.assertTrue(await PMSContact.exists(contact.name))
        self.assertIsNotNone(contact.user)

    @runnify
    async def test_user_is_created_when_mobile_is_specified(self):
        contact = PMSContact(dict(
            first_name="Test A",
            last_name="Test B",
            mobile_no="+966 560440266"
        ))

        await contact.insert()
        await contact.reload()
        self.pms_contacts.add_document(contact)

        self.assertTrue(await PMSContact.exists(contact.name))
        self.assertIsNotNone(contact.user)
        self.assertEqual(contact.user, "966560440266@pms.ae")

    @runnify
    async def test_user_is_deleted_on_contact_delete(self):
        contact = PMSContact(dict(
            first_name="Test A",
            last_name="Test B",
            email_id="test@test.com"
        ))

        await contact.insert()
        await contact.reload()
        self.pms_contacts.add_document(contact)

        import frappe  # TODO: Remove
        self.assertIsNotNone(contact.user)
        self.assertTrue(frappe.db.exists("User", contact.user))

        await contact.delete()
        self.assertFalse(frappe.db.exists("User", contact.user))
