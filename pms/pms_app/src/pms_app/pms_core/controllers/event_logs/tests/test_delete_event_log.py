import unittest
from asyncer import runnify
import renovation

from ..delete_event_log import delete_event_log, PMSContactNotFound, EventLog
from pms_app.pms_core.models.event_log.test_event_log import EventLogFixtures
from pms_app.pms_core.models.pms_contact.test_pms_contact import PMSContactFixtures, PMSContact


class TestDeleteEventLog(unittest.TestCase):

    pms_contacts = PMSContactFixtures(make_users=True)
    event_logs = EventLogFixtures()

    @classmethod
    @runnify
    async def setUpClass(cls):
        await cls.pms_contacts.setUp()

    @classmethod
    @runnify
    async def tearDownClass(cls) -> None:
        await cls.pms_contacts.tearDown()

    @runnify
    async def setUp(self):
        await self.event_logs.setUp()

    @runnify
    async def tearDown(self):
        if renovation.user != "Administrator":
            renovation.set_user("Administrator")
        await self.event_logs.tearDown()

    @runnify
    async def test_delete_simple_concern(self):
        event_log = (await EventLog.get_all(
            fields=["name", "created_by"],
            filters=dict(parent_log=["is", "set"]),
            order_by="creation asc"))[0]
        self.assertIsNotNone(event_log)

        user = await PMSContact.db_get_value(event_log.created_by, "user")
        self.assertIsNotNone(user)
        renovation.set_user(user)

        r = await delete_event_log(event_log)
        self.assertTrue(r)

        self.assertFalse(await EventLog.exists(event_log))

    @runnify
    async def test_administrator_will_throw_with_pms_contact_not_found(self):
        with self.assertRaises(PMSContactNotFound):
            await delete_event_log("random")

    @runnify
    async def test_delete_different_pms_contact(self):
        from pms_app.pms_core import OnlyTheCreatorCanDeleteEventLog
        event_log = (await EventLog.get_all(
            fields=["name", "created_by"],
            filters=dict(parent_log=["is", "set"]),
            order_by="creation asc"))[0]
        self.assertIsNotNone(event_log)

        some_other_contact = await PMSContact.db_get_value(dict(name=["!=", event_log.created_by]))
        self.assertNotEqual(some_other_contact, event_log.created_by)

        user = await PMSContact.db_get_value(some_other_contact, "user")
        self.assertIsNotNone(user)
        renovation.set_user(user)

        with self.assertRaises(OnlyTheCreatorCanDeleteEventLog):
            await delete_event_log(event_log)
