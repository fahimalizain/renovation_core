import unittest
from asyncer import runnify
from renovation.tests import RenovationTestFixture

from .event_type import make_default_event_types, EventType, EventTypes


class EventTypeTestFixtures(RenovationTestFixture):
    def __init__(self):
        super().__init__()
        self.DEFAULT_MODEL = EventType

    async def make_fixtures(self):
        docs = make_default_event_types()
        for d in docs:
            self.add_document(d)


class TestMakeDefaultEventTypes(unittest.TestCase):
    @runnify
    async def test_make_default_event_types(self):
        self.assertFalse(await EventType.exists(EventTypes.CONCERN.value))
        await make_default_event_types()
        self.assertTrue(await EventType.exists(EventTypes.CONCERN.value))

        concern_event_type = await EventType.get_doc(EventTypes.CONCERN.value)
        self.assertGreater(len(concern_event_type.actions.split("\n")), 0)

        for event_type in await EventType.get_all():
            await (await EventType.get_doc(event_type.name)).delete()
