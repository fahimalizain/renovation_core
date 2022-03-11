
import renovation
import frappe
from frappe.model.base_document import BaseDocument

from pms_app.pms_core import PMSContactNotFound, MissingContactInfo
from pms_app.pms_core.models.pms_contact.pms_contact import PMSContact
from pms_app.utils import PermissionDenied, strip_default_fields


async def add_contact(data: dict):
    """
    Please pass company_representative_contact's data as an obj in
    data.company_representative_contact
    """

    if not frappe.has_permission("PMS Contact", ptype="create"):
        raise PermissionDenied(
            message=renovation._("Permission Denied to create PMS Contact"),
            doctype="Contact",
            user=frappe.session.user
        )

    doc = PMSContact()
    _update_pms_contact(data=data, doc=doc)
    _update_company_representative(data.get("company_representative_contact"), doc)

    await doc.insert()

    return await get_contact(doc.name)


async def update_contact(pms_contact: str, data: dict):
    if not frappe.has_permission("PMS Contact", ptype="write"):
        raise PermissionDenied(
            message=renovation._("Permission Denied to update PMS Contact"),
            doctype="PMS Contact",
            user=frappe.session.user
        )

    if not frappe.db.exists("PMS Contact", pms_contact):
        raise PMSContactNotFound(pms_contact=pms_contact)

    doc = await PMSContact.get_doc(pms_contact)
    _update_pms_contact(data=data, doc=doc)
    _update_company_representative(data.get("company_representative_contact"), doc)

    await doc.save()
    return await get_contact(doc.name)


async def delete_contact(pms_contact: str):
    if not frappe.has_permission("PMS Contact", ptype="delete"):
        raise PermissionDenied(
            message=renovation._("Permission Denied to delete PMS Contact"),
            doctype="PMS Contact",
            user=frappe.session.user
        )

    if not await PMSContact.exists(pms_contact):
        raise PMSContactNotFound(pms_contact=pms_contact)

    doc = await PMSContact.get_doc(pms_contact)
    await doc.delete()

    # TODO: Handle Contact
    if doc.get("company_representative_contact") and frappe.db.exists(
            "Contact", doc.get("company_representative_contact")):
        frappe.delete_doc(
            "Contact", doc.get("company_representative_contact"), ignore_permissions=1)


async def get_contact(pms_contact_name):
    return strip_default_fields(await PMSContact.get_doc(pms_contact_name))


def _update_pms_contact(data: dict, doc: BaseDocument):
    doc.update(dict(
        enabled=1,
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        email_id=data.get("email_id"),
        mobile_no=data.get("mobile_no"),
        contact_type=data.get("contact_type")))


def _update_company_representative(data: dict, pms_contact_doc: BaseDocument):
    import frappe  # TODO: FIXME Make RenovationModel for Contact

    if not data:
        return None

    if pms_contact_doc.get("company_representative_contact"):
        contact = frappe.get_doc("Contact", pms_contact_doc.get("company_representative_contact"))
    else:
        contact = frappe.new_doc("Contact")

    for df in ("first_name", "middle_name", "last_name"):
        if df not in data:
            continue
        contact.set(df, data.get(df))

    if not data.get("email_id"):
        data["email_id"] = pms_contact_doc.get("email_id")
    if not data.get("mobile_no"):
        data["mobile_no"] = pms_contact_doc.get("mobile_no")

    if data.get("email_id"):
        contact.email_ids = []
        contact.append("email_ids", dict(
            email_id=data.get("email_id"), is_primary=1
        ))

    if data.get("mobile_no"):
        contact.phone_nos = []
        contact.append("phone_nos", dict(
            phone=data.get("mobile_no"), is_primary_phone=1
        ))

    if not len(contact.get("phone_nos")) or not len(contact.get("email_ids")):
        raise MissingContactInfo(message=renovation._(
            "Please provide Email ID & Mobile No when making a Company Representative"),
            data=renovation._dict(
                doctype="Contact",
                mobile_no_provided=bool(len(contact.get("phone_nos"))),
                email_id_provided=bool(len(contact.get("email_ids"))),
        ))

    contact.save(ignore_permissions=True)
    pms_contact_doc.company_representative_contact = contact.name
