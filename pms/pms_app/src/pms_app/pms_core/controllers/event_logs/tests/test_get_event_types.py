from unittest import TestCase
from asyncer import runnify
from pms_app.pms_core.models.event_type.test_event_type import EventTypeTestFixtures
from pms_app.pms_core.models.pms_contact.pms_contact import PMSContact
from pms_app.pms_core.models.pms_contact.test_pms_contact import PMSContactFixtures
import renovation

from ..get_event_types import get_event_types


class TestGetEventTypes(TestCase):
    event_types = EventTypeTestFixtures(make_default=False)
    pms_contacts = PMSContactFixtures(make_users=True)

    @classmethod
    @runnify
    async def setUpClass(cls) -> None:
        await cls.event_types.setUp()
        await cls.pms_contacts.setUp()

    @classmethod
    @runnify
    async def tearDownClass(cls) -> None:
        if renovation.user != "Administrator":
            renovation.set_user("Administrator")
        await cls.event_types.tearDown()
        await cls.pms_contacts.tearDown()

    @runnify
    async def test_administrator_get_event_types(self):
        t = await get_event_types("Unit")
        should_haves_on_unit = [
            self.event_types.OPEN_TO_ALL_ON_ANYTHING,
            self.event_types.OPEN_TO_ALL_ON_UNIT,
            self.event_types.WATCHMAN_EXCLUSIVE_ON_ANY_MODEL,
            self.event_types.PM_EXCLUSIVE_ON_UNIT]

        self.assertCountEqual(should_haves_on_unit, [x.name for x in t])

        t = await get_event_types("RANDOM")
        should_haves_on_random = [
            self.event_types.OPEN_TO_ALL_ON_ANYTHING,
            self.event_types.WATCHMAN_EXCLUSIVE_ON_ANY_MODEL
        ]
        self.assertCountEqual(should_haves_on_random, [x.name for x in t])

    @runnify
    async def test_watchman(self):
        watchman1 = await PMSContact.db_get_value({"contact_type": "Watchman"}, "user")
        self.assertIsNotNone(watchman1)
        renovation.set_user(watchman1)

        t = await get_event_types("Unit")
        should_haves_on_unit = [
            self.event_types.OPEN_TO_ALL_ON_ANYTHING,
            self.event_types.OPEN_TO_ALL_ON_UNIT,
            self.event_types.WATCHMAN_EXCLUSIVE_ON_ANY_MODEL,
        ]

        self.assertCountEqual(should_haves_on_unit, [x.name for x in t])

        t = await get_event_types("RANDOM")
        should_haves_on_random = [
            self.event_types.OPEN_TO_ALL_ON_ANYTHING,
            self.event_types.WATCHMAN_EXCLUSIVE_ON_ANY_MODEL,
        ]

        self.assertCountEqual(should_haves_on_random, [x.name for x in t])

    @runnify
    async def test_property_manager(self):
        pm1 = await PMSContact.db_get_value({"contact_type": "Property Manager"}, "user")
        self.assertIsNotNone(pm1)
        renovation.set_user(pm1)

        t = await get_event_types("Unit")
        should_haves_on_unit = [
            self.event_types.OPEN_TO_ALL_ON_ANYTHING,
            self.event_types.OPEN_TO_ALL_ON_UNIT,
            self.event_types.PM_EXCLUSIVE_ON_UNIT,
        ]

        self.assertCountEqual(should_haves_on_unit, [x.name for x in t])

        t = await get_event_types("RANDOM")
        should_haves_on_random = [
            self.event_types.OPEN_TO_ALL_ON_ANYTHING,
        ]

        self.assertCountEqual(should_haves_on_random, [x.name for x in t])
