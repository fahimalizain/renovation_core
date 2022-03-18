import renovation


class ActivePMSContact(renovation._dict):
    name: str
    first_name: str
    user: str
    contact_type: str


async def get_current_pms_contact() -> ActivePMSContact:
    from pms_app.pms_core.models.pms_contact.pms_contact import PMSContact

    if hasattr(renovation.local, "pms_contact"):
        contact = renovation.local.pms_contact
        if renovation.user == contact.user:
            # SafetyCheck, in-case set_user was called sometime in between
            return contact

    contact = await PMSContact.db_get_value(
        {"user": renovation.user},
        fieldname=["name", "first_name", "user", "contact_type", "enabled"], as_dict=1)
    if not contact or not contact.enabled:
        return None

    contact = ActivePMSContact(**contact)
    renovation.local.pms_contact = contact
    return contact
