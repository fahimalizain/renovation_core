from typing import Optional

import frappe


def get_contact_type_from_enum(property_type: Optional[str]):
    if not property_type or not len(property_type):
        return None

    property_types = frappe.get_meta("PMS Contact").get_field("contact_type").options.split("\n")
    return next(iter(
        [x for x in property_types if frappe.scrub(x).upper() == property_type]
    ), None)
