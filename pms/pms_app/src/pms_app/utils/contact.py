import renovation
from typing import TypedDict


class ActivePMSContact(TypedDict):
    name: str
    first_name: str
    user: str
    contact_type: str


async def get_current_pms_contact() -> ActivePMSContact:
    from pms_app.pms_core.models.pms_contact.pms_contact import PMSContact

    if hasattr(renovation.local, "pms_contact"):
        return ActivePMSContact(renovation.local.pms_contact)

    contact = await PMSContact.db_get_value(
        {"user": renovation.user},
        fieldname=["name", "first_name", "user", "contact_type"], as_dict=1)
    if not contact:
        return ActivePMSContact()

    contact = ActivePMSContact(**contact)
    renovation.local.pms_contact = contact
    return contact
