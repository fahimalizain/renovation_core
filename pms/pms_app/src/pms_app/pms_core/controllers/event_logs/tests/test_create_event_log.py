import unittest
from asyncer import runnify
import renovation

from ..create_event_log import create_event_log, EventLogData, PMSContactNotFound, EventLog
from pms_app.pms_core.models.event_log.test_event_log import EventLogFixtures
from pms_app.pms_core.models.pms_contact.test_pms_contact import PMSContactFixtures, PMSContact


class TestCreateEventLog(unittest.TestCase):

    pms_contacts = PMSContactFixtures(make_users=True)
    event_logs = EventLogFixtures()

    @runnify
    async def setUp(self):
        await self.pms_contacts.setUp()
        await self.event_logs.setUp()

    @runnify
    async def tearDown(self):
        if renovation.user != "Administrator":
            renovation.set_user("Administrator")
        await self.event_logs.tearDown()
        await self.pms_contacts.tearDown()

    @runnify
    async def test_make_simple_concern(self):
        watchman1 = await PMSContact.db_get_value({"contact_type": "Watchman"}, "user")
        self.assertIsNotNone(watchman1)
        renovation.set_user(watchman1)

        log = await create_event_log(EventLogData(
            entity=self.pms_contacts[0].name,
            entity_type="PMS Contact",
            attachment=None,
            content="He is a loud neighbor!",
            event_type="Concern",
        ))

        self.assertTrue(await EventLog.exists(log.name))
        self.assertEqual(log.event_type, "Concern")
        self.event_logs.add_document(log)

    @runnify
    async def test_administrator_will_throw_with_pms_contact_not_found(self):
        with self.assertRaises(PMSContactNotFound):
            await create_event_log(EventLogData(
                entity=self.pms_contacts[0].name,
                entity_type="PMS Contact",
                attachment=None,
                content="He is a loud neighbor!",
                event_type="Concern"
            ))
