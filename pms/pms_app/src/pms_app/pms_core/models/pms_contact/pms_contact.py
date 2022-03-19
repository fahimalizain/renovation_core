import re
from asyncer import asyncify
from renovation import RenovationModel
from .pms_contact_types import PMSContactMeta


class PMSContact(RenovationModel["PMSContact"], PMSContactMeta):
    async def validate(self):
        await self.update_user()

    async def on_trash(self):
        if self.user:
            # unlink
            await PMSContact.db_set_value(self.name, "user", None)

            import frappe
            await asyncify(frappe.delete_doc)("User", self.user)
            await self.reload()

    async def update_user(self):
        # TODO: Handle User Doctype through Renovation
        import frappe

        if self.user:
            user = await asyncify(frappe.get_doc)("User", self.user)
        else:
            if not self.email_id and not self.mobile_no:
                return

            email_id = self.email_id
            if not email_id and self.mobile_no:
                email_id = re.sub(r"[^\d]", "", self.mobile_no) + "@pms.ae"

            user = frappe.get_doc(dict(
                doctype="User",
                email=email_id,
            ))

        user.first_name = self.first_name
        user.last_name = self.last_name
        user.enabled = self.enabled
        user.roles = []
        user.append("roles", dict(role="PMS Contact"))
        user.append("roles", dict(role=self.contact_type))

        await asyncify(user.save)(ignore_permissions=True)
        if not self.user:
            self.user = user.name
