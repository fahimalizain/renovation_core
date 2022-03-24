from unittest import TestCase
from asyncer import runnify
from pms_app.pms_core.models.pms_contact.test_pms_contact import PMSContactFixtures
from pms_app.pms_core.models.pms_custom_field.pms_custom_field import PMSCustomField
from pms_app.utils.exceptions import PermissionDenied
import renovation

from ..create_custom_field import create_custom_field


class TestCreateCustomField(TestCase):
    pms_contacts = PMSContactFixtures(make_users=True)

    @runnify
    async def setUp(self) -> None:
        await self.pms_contacts.setUp()

    @runnify
    async def tearDown(self) -> None:
        if renovation.user != "Administrator":
            renovation.set_user("Administrator")
        await self.pms_contacts.tearDown()

    @runnify
    async def test_create_simple(self):
        r = await create_custom_field(dict(
            label="Test A",
            fieldtype="Data",
            entity_type="PMS Contact"
        ))
        self.assertIsNotNone(r)
        self.assertTrue(await PMSCustomField.exists(r.name))
        self.assertEqual(r.fieldname, renovation.scrub("Test A"))

        await r.delete()

    @runnify
    async def test_sys_admin(self):
        pms_contact = self.pms_contacts[0]
        renovation.set_user(pms_contact.user)
        with self.assertRaises(PermissionDenied):
            await create_custom_field(dict(
                label="Test A",
                fieldtype="Data",
                entity_type="PMS Contact"
            ))

        # Add Sys Admin role to Contact's user
        import frappe
        user = frappe.get_doc("User", pms_contact.user)
        user.append("roles", dict(role="Sys Admin"))
        user.save(ignore_permissions=True)

        r = await create_custom_field(dict(
            label="Test A",
            fieldtype="Data",
            entity_type="PMS Contact"
        ))
        self.assertIsNotNone(r)
        self.assertTrue(await PMSCustomField.exists(r.name))
        self.assertEqual(r.fieldname, renovation.scrub("Test A"))

        await r.delete()
