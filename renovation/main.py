import os

import uvicorn
from fastapi import FastAPI
from graphql import GraphQLError
import frappe
from renovation_core.graphql import execute, log_error
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

    @fastapi_app.post("/graphql")
    async def graphql_resolver(body: dict):
        graphql_request = frappe.parse_json(body)
        query = graphql_request.query
        variables = graphql_request.variables
        operation_name = graphql_request.operationName
        output = await execute(query, variables, operation_name)
        if len(output.get("errors", [])):
            log_error(query, variables, operation_name, output)
            errors = []
            for err in output.errors:
                if isinstance(err, GraphQLError):
                    err = err.formatted
                errors.append(err)
            output.errors = errors
            errors = []
            for err in output.errors:
                if isinstance(err, GraphQLError):
                    err = err.formatted
                errors.append(err)
            output.errors = errors
        return output

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

# if __name__ == "__main__":
#     uvicorn.run("renovation.main:app", host="0.0.0.0", port=8004, loop="uvloop", workers=None)
