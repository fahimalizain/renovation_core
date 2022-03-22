import unittest
from asyncer import runnify
from renovation.tests import RenovationTestFixture

from .event_type import make_default_event_types, EventType, EventTypes


class EventTypeTestFixtures(RenovationTestFixture):

    OPEN_TO_ALL_ON_ANYTHING = "Open-To-All-On-Anything"
    WATCHMAN_EXCLUSIVE_ON_ANY_MODEL = "W-Exclusive-Any-MODEL"
    PM_EXCLUSIVE_ON_UNIT = "PM-Exclusive-ON-UNIT"
    OPEN_TO_ALL_ON_UNIT = "Open-To-All-On-Unit"

    def __init__(self, make_default=True):
        super().__init__()
        self.DEFAULT_MODEL = EventType
        self.make_default = make_default

    async def make_fixtures(self):
        if self.make_default:
            docs = await make_default_event_types()
            for d in docs:
                self.add_document(d)
        else:
            docs = []

            # A type that could be made by anyone on anything
            docs.append(dict(
                title=self.OPEN_TO_ALL_ON_ANYTHING,
                roles=[dict(role="PMS Contact")]
            ))

            # A Type which could be made only by watchman on any model
            docs.append(dict(
                title=self.WATCHMAN_EXCLUSIVE_ON_ANY_MODEL,
                roles=[dict(role="Watchman")],
            ))

            # PM Exclusive on Unit
            docs.append(dict(
                title=self.PM_EXCLUSIVE_ON_UNIT,
                roles=[dict(role="Property Manager")],
                models=[dict(model="Unit")],
            ))

            # Open to all on Unit
            docs.append(dict(
                title=self.OPEN_TO_ALL_ON_UNIT,
                roles=[dict(role="PMS Contact")],
                models=[dict(model="Unit")]
            ))

            for d in docs:
                self.add_document(await EventType(d).insert())


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
