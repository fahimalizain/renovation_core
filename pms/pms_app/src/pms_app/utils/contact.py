import renovation
from pms_app.pms_core.models.pms_contact.pms_contact import PMSContact


async def get_current_pms_contact():
    if hasattr(renovation.local, "pms_contact"):
        return renovation.local.pms_contact

    contact = await PMSContact.db_get_value({"user": renovation.user}, fieldname=["name", "first_name", ""])
    if not contact:
        return None

    renovation.local.pms_contact = contact
    return contact
