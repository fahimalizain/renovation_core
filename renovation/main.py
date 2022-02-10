import os
from fastapi import FastAPI

import frappe
from .frappehandler import FrappeMiddleware


def get_app():
    fastapi_app = FastAPI()
    fastapi_app.add_middleware(FrappeMiddleware)

    @fastapi_app.get("/info")
    def read_root():
        available_doctypes = frappe.get_list("DocType")
        settings = frappe.get_single("System Settings")
        return {
            "available_doctypes": available_doctypes,
            "settings": settings.as_dict(),
        }

    renovation_apps = []
    # Load Frappe ORMs
    for app in frappe.get_all_apps(with_internal_apps=False, sites_path=os.getcwd()):
        renovation_app = getattr(frappe.get_module(app + ".hooks"), "renovation_app", None)
        if not renovation_app:
            continue

        renovation_apps.append(renovation_app)
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

                doctype_module = f"{app}.{module}.doctype.{doctype}.{doctype}"
                print("Importing ", doctype_module)
                frappe.get_module(doctype_module)

    # Load Renovation App Routers
    for app in renovation_apps:
        router = getattr(frappe.get_module(f"{app}.api"), "router", None)
        if router:
            fastapi_app.include_router(router)

    return fastapi_app


app = get_app()
