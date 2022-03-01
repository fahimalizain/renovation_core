import os

import frappe
import json


def load_renovation_app_info():

    info = frappe._dict(
        apps=[],
        app_doctypes=frappe._dict(),
        frappe_app_map=frappe._dict()
    )

    for app in frappe.get_installed_apps():
        renovation_app = getattr(frappe.get_module(app + ".hooks"), "renovation_app", None)
        if not renovation_app:
            continue

        info.apps.append(renovation_app)
        info.frappe_app_map[renovation_app] = app
        info.app_doctypes[renovation_app] = []
        for module in frappe.get_module_list(app):
            module = frappe.scrub(module)
            module_path = frappe.get_pymodule_path(app, module)
            doctypes_path = os.path.join(module_path, "doctype")
            if not os.path.exists(doctypes_path):
                continue

            for doctype in os.listdir(doctypes_path):
                if not os.path.isdir(os.path.join(doctypes_path, doctype)):
                    continue
                doctype_json = os.path.join(doctypes_path, doctype, doctype + ".json")
                if not os.path.exists(doctype_json):
                    continue

                frappe.parse_json
                doctype_module = f"{app}.{module}.doctype.{doctype}.{doctype}"
                print("Importing ", doctype_module)
                frappe.get_module(doctype_module)

                with open(doctype_json) as j:
                    meta = json.load(j)
                    info.app_doctypes[renovation_app].append(meta.get("name"))

    frappe.cache().set_value("renovation_app_info", info)
    return info


def get_renovation_app_info():
    info = frappe.cache().get_value("renovation_app_info")
    if not info:
        load_renovation_app_info()
        return get_renovation_app_info()

    return info


def get_renovation_apps():
    info = get_renovation_app_info()
    return info.apps


def is_renovation_doctype(doctype: str):
    info = get_renovation_app_info()
    for app in info.apps:
        if doctype in info.app_doctypes.get(app, []):
            return True

    return False


def get_doctype_renovation_app(doctype: str):
    info = get_renovation_app_info()
    for app in info.apps:
        if doctype in info.app_doctypes.get(app, []):
            return app

    return None
