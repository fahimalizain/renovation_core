from unittest import TestCase
from asyncer import runnify
from pms_app.pms_core.models.event_log.event_log import EventLog
from pms_app.pms_core.models.pms_contact.pms_contact import PMSContact

from ..get_event_thread import get_event_thread
from pms_app.pms_core.models.event_log.test_event_log import EventLogFixtures


class TestGetEventThread(TestCase):
    event_logs = EventLogFixtures()

    @runnify
    async def setUp(self) -> None:
        await self.event_logs.setUp()

    @runnify
    async def tearDown(self) -> None:
        await self.event_logs.tearDown()

    @runnify
    async def test_simple_get_event_thread(self):
        parent_log = (await EventLog.get_all(
            {"parent_log": ["is", "set"]}, "parent_log"))[0].parent_log
        self.assertIsNotNone(parent_log)

        event_logs = await get_event_thread(parent_log)

        self.assertGreater(len(event_logs), 1)
        for log in event_logs:
            if log.parent_log:
                self.assertEqual(log.parent_log, parent_log)
            else:
                self.assertEqual(log.name, parent_log)

            self.assertIsNotNone(log.content)
            self.assertTrue(await PMSContact.exists(log.created_by))
