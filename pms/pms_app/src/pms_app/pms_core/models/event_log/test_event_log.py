import unittest
from asyncer import runnify
from renovation import _dict
import renovation
from renovation.tests import RenovationTestFixture

from .event_log import EventLog
from ..event_type.test_event_type import EventTypeTestFixtures, EventTypes
from ..pms_contact.test_pms_contact import PMSContactFixtures, PMSContact
from pms_app.properties.models.unit.test_unit import UnitFixtures, Unit


class EventLogFixtures(RenovationTestFixture):

    pms_contacts = PMSContactFixtures(make_users=True)

    def __init__(self):
        super().__init__()
        self.DEFAULT_MODEL = EventLog
        self.dependent_fixtures = [EventTypeTestFixtures, UnitFixtures]

    async def setUp(self, skip_fixtures=False, skip_dependencies=False):
        await self.pms_contacts.setUp()
        await super().setUp(skip_fixtures, skip_dependencies)
        self._dependent_fixture_instances.append(self.pms_contacts)

    async def tearDown(self):
        await super().tearDown()
        await self.pms_contacts.tearDown()

    async def make_fixtures(self):
        await self.make_watchman_concern()
        await self.make_owner_concern()

    async def delete_fixtures(self):
        """
        EventLogs require the created-pms-contact to delete it
        """
        original_user = str(renovation.user)
        for model, docs in self.fixtures.items():
            _docs = list(docs)
            _docs.reverse()
            for doc in _docs:
                if not await model.exists(doc.name) or doc is None:
                    continue

                await doc.reload()
                user = await PMSContact.db_get_value(doc.created_by, "user")
                renovation.set_user(user)
                await doc.delete(ignore_permissions=True)

        self.fixtures = renovation._dict()
        renovation.set_user(original_user)

    async def make_watchman_concern(self):
        watchman1 = await PMSContact.db_get_value({"contact_type": "Watchman"})
        units = self.get_dependencies(Unit)

        d = EventLog(_dict(
            entity_type=Unit.get_doctype(),
            entity=units[0].name,
            event_type=EventTypes.CONCERN.value,
            created_by=watchman1,
            content="Test Concern 1"
        ))
        await d.insert()
        self.add_document(d)

        d1 = EventLog(_dict(
            entity_type=Unit.get_doctype(),
            entity=units[0].name,
            event_type=EventTypes.CONCERN.value,
            created_by=watchman1,
            parent_log=d.name,
            content="Test Reply 1"
        ))
        await d1.insert()
        self.add_document(d1)

    async def make_owner_concern(self):
        owner1 = await PMSContact.db_get_value({"contact_type": "Property Owner"})
        units = self.get_dependencies(Unit)

        d = EventLog(_dict(
            entity_type=Unit.get_doctype(),
            entity=units[0].name,
            event_type=EventTypes.CONCERN.value,
            created_by=owner1,
            content="Test Concern 1"
        ))
        await d.insert()
        self.add_document(d)

        d1 = EventLog(_dict(
            entity_type=Unit.get_doctype(),
            entity=units[0].name,
            event_type=EventTypes.CONCERN.value,
            created_by=owner1,
            parent_log=d.name,
            content="Test Reply 1"
        ))
        await d1.insert()
        self.add_document(d1)


class TestEventLog(unittest.TestCase):
    event_logs = EventLogFixtures()

    @classmethod
    @runnify
    async def setUpClass(self):
        await self.event_logs.setUp()

    @classmethod
    @runnify
    async def tearDownClass(self):
        await self.event_logs.tearDown()

    @runnify
    async def test_set_parent_as_another_child(self):
        from pms_app.pms_core import EventLogParentIsNotRootLog
        child_logs = await EventLog.get_all({"parent_log": ["is", "set"]})

        d1 = EventLog(_dict(
            entity_type=Unit.get_doctype(),
            entity=self.event_logs.get_dependencies(Unit)[0].name,
            event_type=EventTypes.CONCERN.value,
            created_by=self.event_logs.get_dependencies(PMSContact)[0].name,
            parent_log=child_logs[0].name,
            content="Test Reply 1"
        ))

        with self.assertRaises(EventLogParentIsNotRootLog):
            await d1.insert()

    @runnify
    async def test_setting_primary_on_child(self):
        from pms_app.pms_core import PrimaryEventLogCanOnlyBeSetOnRootLog
        child_logs = await EventLog.get_all({"parent_log": ["is", "set"]})
        parent_logs = await EventLog.get_all({"parent_log": ["is", "not set"]})

        child_log = await EventLog.get_doc(child_logs[0].name)
        child_log.primary_log = parent_logs[0].name

        with self.assertRaises(PrimaryEventLogCanOnlyBeSetOnRootLog):
            await child_log.save()

    @runnify
    async def test_set_primary_that_belongs_to_another_thread(self):
        from pms_app.pms_core import PrimaryEventLogDoNotBelongToCurrentThread
        child_logs = await EventLog.get_all({"parent_log": ["is", "set"]}, ["name", "parent_log"])
        parent_logs = await EventLog.get_all({"parent_log": ["is", "not set"]})

        parent_log = await EventLog.get_doc(parent_logs[0].name)
        parent_log.primary_log = [x for x in child_logs if x.parent_log != parent_log.name][0].name

        with self.assertRaises(PrimaryEventLogDoNotBelongToCurrentThread):
            await parent_log.save()

    @runnify
    async def test_disabled_contact(self):
        from pms_app.pms_core import PMSContactDisabled
        contact = self.event_logs.get_dependencies(PMSContact)[0]
        contact.enabled = 0
        await contact.save()

        d1 = EventLog(_dict(
            entity_type=Unit.get_doctype(),
            entity=self.event_logs.get_dependencies(Unit)[0].name,
            event_type=EventTypes.CONCERN.value,
            created_by=contact.name,
            content="Test Reply 1"
        ))

        with self.assertRaises(PMSContactDisabled):
            await d1.save()

        contact.enabled = 1
        await contact.save()

    @runnify
    async def test_contact_with_no_user(self):
        from pms_app.pms_core import PMSContactUserUnavailable
        contact = self.event_logs.get_dependencies(PMSContact)[0]
        _user = contact.user
        await PMSContact.db_set_value(contact.name, "user", None)

        d1 = EventLog(_dict(
            entity_type=Unit.get_doctype(),
            entity=self.event_logs.get_dependencies(Unit)[0].name,
            event_type=EventTypes.CONCERN.value,
            created_by=contact.name,
            content="Test Reply 1"
        ))

        with self.assertRaises(PMSContactUserUnavailable):
            await d1.save()

        await PMSContact.db_set_value(contact.name, "user", _user)
        await contact.reload()

    # TODO: This particular test case could break the systems on_trash events
    # We need an async renovation.delete_doc
    # @runnify
    # async def test_set_proper_child_as_primary(self):
    #     child_logs = await EventLog.get_all({"parent_log": ["is", "set"]}, ["name", "parent_log"])
    #     parent_logs = await EventLog.get_all({"parent_log": ["is", "not set"]})

    #     parent_log = await EventLog.get_doc(parent_logs[0].name)
    #     proper_child = [x for x in child_logs if x.parent_log == parent_log.name][0].name
    #     parent_log.primary_log = proper_child

    #     await parent_log.save()
    #     self.assertEqual(parent_log.primary_log, proper_child)
