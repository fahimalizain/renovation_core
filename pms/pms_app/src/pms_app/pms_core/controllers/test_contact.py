from unittest import TestCase
# from unittest import IsolatedAsyncioTestCase
from asyncer import runnify

from pms_app.pms_core.models.test_pms_contact import PMSContactFixtures
from .contact import (
    PMSContact,
    add_contact,
    update_contact,
    delete_contact,
    # get_contact,
)


class TestContactAdd(TestCase):

    @runnify
    async def test_simple_insert(self):
        r = await add_contact(dict(
            first_name="Test A"
        ))
        self.assertEqual(r.first_name, "Test A")
        self.assertTrue(await PMSContact.exists(r.name))


class TestContactUpdate(TestCase):
    contacts = PMSContactFixtures()

    @runnify
    async def setUp(self):
        await self.contacts.setUp()

    @runnify
    async def tearDown(self):
        await self.contacts.tearDown()

    @runnify
    async def test_simple_update(self):
        pms_contact = self.contacts[0]
        new_name = "Test 233445"

        await update_contact(pms_contact.name, dict(
            first_name=new_name
        ))
        self.assertEqual(
            new_name, await PMSContact.db_get_value(pms_contact.name, "first_name"))


class TestContactDelete(TestCase):
    contacts = PMSContactFixtures()

    @runnify
    async def setUp(self):
        await self.contacts.setUp()

    @runnify
    async def tearDown(self):
        await self.contacts.tearDown()

    @runnify
    async def test_simple_delete(self):
        pms_contact = self.contacts[0]
        _exists = await PMSContact.exists(pms_contact.name)
        self.assertTrue(_exists)

        await delete_contact(pms_contact.name)
        _exists = await PMSContact.exists(pms_contact.name)
        self.assertFalse(_exists)
