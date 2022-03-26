from unittest import TestCase
from asyncer import runnify
from pms_app.utils.exceptions import PermissionDenied

import renovation
from ..get_customizable_entity_types import get_customizable_entity_types
from pms_app.pms_core.models.pms_contact.test_pms_contact import PMSContactFixtures
from pms_app.pms_core.models.pms_custom_field.pms_custom_field import \
    PMS_CUSTOMIZABLE_ENTITY_TYPES_HOOK


class TestGetCustomizableEntityTypes(TestCase):
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
    async def test_sys_admin(self):
        pms_contact = self.pms_contacts[0]
        renovation.set_user(pms_contact.user)

        with self.assertRaises(PermissionDenied):
            await get_customizable_entity_types()

        # Add Sys Admin role to Contact's user
        import frappe
        user = frappe.get_doc("User", pms_contact.user)
        user.append("roles", dict(role="Sys Admin"))
        user.save(ignore_permissions=True)

        r = await get_customizable_entity_types()
        self.assertGreater(len(r), 0)

        _types = list(set(renovation.get_hooks(PMS_CUSTOMIZABLE_ENTITY_TYPES_HOOK)))

        self.assertCountEqual(_types, r)
