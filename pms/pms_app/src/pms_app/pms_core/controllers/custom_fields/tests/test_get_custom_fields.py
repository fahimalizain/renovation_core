from functools import reduce
from unittest import TestCase
from asyncer import runnify

from pms_app.pms_core.models.pms_contact.test_pms_contact import PMSContactFixtures
from pms_app.pms_core.models.pms_custom_field.pms_custom_field import PMSCustomField
from pms_app.pms_core.models.pms_custom_field.test_pms_custom_field import PMSCustomFieldTestFixture
from pms_app.utils.exceptions import InvalidArguments, PermissionDenied
import renovation

from ..get_custom_fields import get_custom_fields


class TestGetCustomFields(TestCase):
    pms_contacts = PMSContactFixtures(make_users=True)
    custom_fields = PMSCustomFieldTestFixture()

    @runnify
    async def setUp(self) -> None:
        await self.pms_contacts.setUp()
        await self.custom_fields.setUp()

    @runnify
    async def tearDown(self) -> None:
        if renovation.user != "Administrator":
            renovation.set_user("Administrator")
        await self.custom_fields.tearDown()
        await self.pms_contacts.tearDown()

    @runnify
    async def test_get_simple(self):

        r = await get_custom_fields()

        self.assertIsNotNone(r)
        self.assertGreater(len(r), 0)

        for cf in r:
            self.assertTrue(await PMSCustomField.exists(cf.name))

    @runnify
    async def test_sys_admin(self):
        pms_contact = self.pms_contacts[0]
        renovation.set_user(pms_contact.user)

        with self.assertRaises(PermissionDenied):
            await get_custom_fields()

        # Add Sys Admin role to Contact's user
        import frappe
        user = frappe.get_doc("User", pms_contact.user)
        user.append("roles", dict(role="Sys Admin"))
        user.save(ignore_permissions=True)

        r = await get_custom_fields()

        self.assertIsNotNone(r)
        self.assertGreater(len(r), 0)

        got_one_entities_excluded = False
        for cf in r:
            self.assertTrue(await PMSCustomField.exists(cf.name))
            self.assertIsInstance(cf.entities_excluded, list)
            if len(cf.entities_excluded):
                got_one_entities_excluded = True
                for m in cf.entities_excluded:
                    self.assertIsInstance(m, str)

        self.assertTrue(got_one_entities_excluded)

    @runnify
    async def test_only_entity_arg(self):
        with self.assertRaises(InvalidArguments):
            await get_custom_fields(entity="Test A")

    @runnify
    async def test_entity_type(self):
        r = await get_custom_fields(entity_type=self.custom_fields.TEST_ENTITY_TYPE)
        self.assertGreater(len(r), 0)

        # None means global Custom Fields
        self.assertCountEqual(
            [None, self.custom_fields.TEST_ENTITY_TYPE],
            list(set([x.entity_type for x in r]))
        )

        # Excluded Entity Test
        all_excluded = set(reduce(lambda arr, cf: (arr.extend(cf.entities_excluded) or arr), r, []))
        self.assertNotIn(self.custom_fields.TEST_ENTITY_TYPE, all_excluded)

    @runnify
    async def test_entity(self):
        r = await get_custom_fields(
            entity_type=self.custom_fields.TEST_ENTITY_TYPE,
            entity=self.custom_fields.TEST_ENTITY)
        self.assertGreater(len(r), 0)

        # None means global Custom Fields
        # entity_type assert
        # Make sure Global Fields did come in
        self.assertCountEqual(
            [None, self.custom_fields.TEST_ENTITY_TYPE],
            list(set([x.entity_type for x in r]))
        )

        # entity assert
        # Make sure EntityType specific fields did come in
        self.assertCountEqual(
            [None, self.custom_fields.TEST_ENTITY],
            list(set([x.entity for x in r]))
        )

    @runnify
    async def test_entities_excluded(self):
        r = await get_custom_fields(
            entity_type=self.custom_fields.NON_EXCLUDED_ENTITY)
        self.assertGreater(len(r), 0)

        all_excluded = set(reduce(lambda arr, cf: (arr.extend(cf.entities_excluded) or arr), r, []))
        self.assertIn(self.custom_fields.TEST_ENTITY_TYPE, all_excluded)
