from unittest import TestCase
from asyncer import runnify
from pms_app.pms_core.models.pms_contact.test_pms_contact import PMSContactFixtures
from pms_app.pms_core.models.pms_custom_field.test_pms_custom_field import PMSCustomFieldTestFixture
from pms_app.utils.exceptions import NotFound, PermissionDenied
import renovation

from ..update_custom_field import update_custom_field


class TestUpdateCustomField(TestCase):
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
        new_label = "TEST ABCDEF"

        r = await update_custom_field(
            custom_field=custom_field.name,
            data=dict(
                label=new_label,
            ))

        await custom_field.reload()
        self.assertIsNotNone(r)
        self.assertEqual(custom_field.label, new_label)
        self.assertEqual(r.label, new_label)

    @runnify
    async def test_sys_admin(self):
        pms_contact = self.pms_contacts[0]
        renovation.set_user(pms_contact.user)

        custom_field = self.custom_fields[0]
        new_label = "TEST ABCDEF"

        with self.assertRaises(PermissionDenied):
            await update_custom_field(
                custom_field=custom_field.name,
                data=dict(
                    label=new_label,
                ))

        # Add Sys Admin role to Contact's user
        import frappe
        user = frappe.get_doc("User", pms_contact.user)
        user.append("roles", dict(role="Sys Admin"))
        user.save(ignore_permissions=True)

        r = await update_custom_field(
            custom_field=custom_field.name,
            data=dict(
                label=new_label,
            ))

        await custom_field.reload()
        self.assertIsNotNone(r)
        self.assertEqual(custom_field.label, new_label)
        self.assertEqual(r.label, new_label)

    @runnify
    async def test_random_custom_field(self):
        with self.assertRaises(NotFound):
            await update_custom_field(
                custom_field="RANDOM-Custom-Field",
                data=dict(
                    label="new_label",
                ))
