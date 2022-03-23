from unittest import TestCase
from asyncer import runnify
from pms_app.pms_core.models.pms_contact.pms_contact import PMSContact

from ..get_events import get_events
from pms_app.pms_core.models.event_log.test_event_log import EventLogFixtures
from pms_app.properties.models.unit.unit import Unit


class TestGetEvents(TestCase):
    event_logs = EventLogFixtures()

    @runnify
    async def setUp(self) -> None:
        await self.event_logs.setUp()

    @runnify
    async def tearDown(self) -> None:
        await self.event_logs.tearDown()

    @runnify
    async def test_simple_get_events(self):
        entity_doc = self.event_logs.get_dependencies(Unit)[0]

        event_logs = await get_events(
            model=entity_doc.get_doctype(),
            name=entity_doc.name
        )

        self.assertGreater(len(event_logs), 0)
        for log in event_logs:
            self.assertEqual(log.entity_type, entity_doc.get_doctype())
            self.assertEqual(log.entity, entity_doc.name)
            self.assertIsNotNone(log.content)
            self.assertTrue(await PMSContact.exists(log.created_by))

    # TODO: Test get_events with a primary log set
