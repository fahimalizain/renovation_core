
import importlib
import os
from typing import Optional

import frappe
from frappe.modules.utils import get_doc_path
from renovation_core.utils.doc_utils import has_table_value_changed

def check_for_renovation_doctype(doctype_doc):
    """Check if the doctype belongs to a 'renovation' app"""

    # Check if there is any need to popagate changes; only need to make changes if fields were changed
    if not has_table_value_changed(doctype_doc, "fields"):
        return

    # Get the app, check if the app is a wrapper-app by checking if is in

    renovation_app_name = get_external_app(frappe.get_doctype_app(doctype_doc.name))

    if not renovation_app_name:
        return

    try:
        importlib.import_module(renovation_app_name)
    except ModuleNotFoundError:
        frappe.throw(
            "This DocType appears to belong to a renovation wrapper-app, "
            f"but the relevant extrenal-app package could not be found: `{renovation_app_name}`."
            " Please ensure it is installed."
        )

def get_external_app(app_name) -> Optional[str]:
    """Checks if an app is a wrapper app thorough the `renovation_app` hook"""

    renovation_app_name = frappe.get_hooks("renovation_app", app_name=app_name)

    if not renovation_app_name:
        return
    else:
        return renovation_app_name[0]

def make_wrapper_app_boilerplate_controller(doc, app_name):
    """Generates a custom [doctype].py controller for the doctype that is linked to an external app"""

    target_path = get_doc_path(doc.module, doc.doctype, doc.name)
    file_name = frappe.scrub(f'{doc.name}.py')
    target_file_path = os.path.join(target_path, file_name)

    with open(target_file_path, 'w') as target:

        with open(os.path.join(frappe.get_app_path("renovation_core"),"overrides/doctype", "controller._py"), 'r') as source:

            target.write(frappe.as_unicode(
                frappe.utils.cstr(source.read()).format(
                        app_name=app_name,
                        scrubbed_doctype=frappe.scrub(doc.name),
                        classname=doc.name.replace(" ", ""),
                        doctype=doc.name
                    )
            ))
