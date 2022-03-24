from unittest import TestCase
from asyncer import runnify
from pms_app.pms_core.models.pms_contact.test_pms_contact import PMSContactFixtures
from pms_app.pms_core.models.pms_custom_field.pms_custom_field import PMSCustomField
from pms_app.pms_core.models.pms_custom_field.test_pms_custom_field import PMSCustomFieldTestFixture
from pms_app.utils.exceptions import NotFound, PermissionDenied
import renovation

from ..delete_custom_field import delete_custom_field


class TestDeleteCustomField(TestCase):
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
    async def test_update_simple(self):
        custom_field = self.custom_fields[0]

        r = await delete_custom_field(
            custom_field=custom_field.name,
        )

        self.assertTrue(r)
        self.assertFalse(await PMSCustomField.exists(custom_field.name))

    @runnify
    async def test_sys_admin(self):
        pms_contact = self.pms_contacts[0]
        renovation.set_user(pms_contact.user)

        custom_field = self.custom_fields[0]

        with self.assertRaises(PermissionDenied):
            await delete_custom_field(
                custom_field=custom_field.name)

        # Add Sys Admin role to Contact's user
        import frappe
        user = frappe.get_doc("User", pms_contact.user)
        user.append("roles", dict(role="Sys Admin"))
        user.save(ignore_permissions=True)

        r = await delete_custom_field(
            custom_field=custom_field.name)

        self.assertTrue(r)
        self.assertFalse(await PMSCustomField.exists(custom_field.name))

    @runnify
    async def test_random_custom_field(self):
        with self.assertRaises(NotFound):
            await delete_custom_field(
                custom_field="RANDOM-Custom-Field")
