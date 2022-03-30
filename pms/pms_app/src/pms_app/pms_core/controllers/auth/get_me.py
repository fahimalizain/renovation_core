import renovation
from pms_app.pms_core.models.pms_contact.pms_contact import PMSContact
PMSContact


async def get_me():
    if renovation.user in ("Guest", "Administrator"):
        return None

    contact = await PMSContact.db_get_value({"user": renovation.user}, [
        "name as pms_contact", "first_name", "last_name", "contact_type", "user"
    ], as_dict=1)

    return contact
