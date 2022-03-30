from unittest import TestCase
from asyncer import runnify

import renovation
from ..get_me import get_me
from pms_app.pms_core.models.pms_contact.test_pms_contact import PMSContactFixtures


class TestGetMe(TestCase):

    pms_contacts = PMSContactFixtures(make_users=True)

    @classmethod
    @runnify
    async def setUpClass(cls):
        await cls.pms_contacts.setUp()

    @classmethod
    @runnify
    async def tearDownClass(cls):
        if renovation.user != "Administrator":
            renovation.set_user("Administrator")
        await cls.pms_contacts.tearDown()

    @runnify
    async def test_admin_guests(self):
        r = await get_me()
        self.assertEqual(r, None)

        renovation.set_user("Guest")
        r = await get_me()
        self.assertEqual(r, None)

    @runnify
    async def test_simple(self):
        pms_contact = self.pms_contacts[0]
        renovation.set_user(pms_contact.user)

        r = await get_me()

        for k in ("pms_contact", "user", "contact_type"):
            self.assertIsNotNone(r.get(k))

        self.assertEqual(r.pms_contact, pms_contact.name)
        self.assertEqual(r.first_name, pms_contact.first_name)
        self.assertEqual(r.contact_type, pms_contact.contact_type)
        self.assertEqual(r.user, pms_contact.user)
