import os
import frappe

import renovation
from .app import is_renovation_frappe_app, get_renovation_app_of_frappe_app


# TODO: Table Fields

def on_doctype_update(doc, method=None):
    make_updates(doctype_doc=doc)


def on_custom_field_update(doc, method=None):
    doctype_doc = frappe.get_doc("DocType", doc.dt)
    make_updates(
        doctype_doc=doctype_doc,
        _types=True,
        renovation_controller=False,
        frappe_controller=False)


def make_updates(
        doctype_doc,
        _types=True,
        renovation_controller=True,
        frappe_controller=True):
    frappe_app = frappe.db.get_value("Module Def", doctype_doc.module, "app_name")
    if not is_renovation_frappe_app(frappe_app):
        return

    renovation_app = get_renovation_app_of_frappe_app(frappe_app)

    # Renovation Target Folder:
    r_dt_folder = os.path.join(
        os.path.dirname(renovation.get_module(renovation_app).__file__),
        renovation.scrub(doctype_doc.module),
        "models",
        renovation.scrub(doctype_doc.name)
    )
    r_dt_module = f"{renovation_app}.{renovation.scrub(doctype_doc.module)}.models." + \
        f"{renovation.scrub(doctype_doc.name)}.{renovation.scrub(doctype_doc.name)}"

    os.makedirs(r_dt_folder, exist_ok=True)

    # Make typed meta class
    if _types:
        generate_types(doctype_doc, r_dt_folder)

    # Make renovation controller
    if renovation_controller:
        handle_renovation_controller(doctype_doc, r_dt_folder)

    # Update frappe controller
    if frappe_controller:
        handle_frappe_controller(doctype_doc, r_dt_module=r_dt_module)


def generate_types(doc, r_dt_folder):
    from frappe.model import display_fieldtypes, numeric_fieldtypes, table_fields

    imports = dict()
    path = os.path.join(r_dt_folder, renovation.scrub(doc.name) + "_types.py")

    def _add_import(_from, _import):
        if _from not in imports:
            imports[_from] = set()

        imports[_from].add(_import)

    _py = f"class {doc.name.replace(' ', '')}Meta:"

    def _add_df(df):
        nonlocal _py

        if df.fieldtype in display_fieldtypes:
            return

        reqd = df.reqd
        df_wip = False  # DF Work In Progress
        _type = "str"
        if df.fieldtype in numeric_fieldtypes:
            _type = "float" if df.fieldtype in ("Currency", "Float", "Percent") else "int"
        elif df.fieldtype in table_fields:
            # TODO: Table
            df_wip = True
            reqd = True
            # _add_import("typing", "List")
            # _add_import(" .. path to child doc .. ")
            _type = f"List[{df.options.replace(' ', '')}]"
        else:
            _type = "str"

        if not reqd:
            _add_import("typing", "Optional")
            _type = f"Optional[{_type}]"

        _py += f"\n    {'# 'if df_wip else ''}{df.fieldname}: {_type}"

    for df in doc.fields:
        _add_df(df)

    custom_fields = frappe.get_all("Custom Field", {"dt": doc.name}, ["*"])
    if len(custom_fields):
        _py += "\n\n    # Custom Fields"
        for df in custom_fields:
            _add_df(df)

    if imports:
        _imports = ""
        for _from, _import in imports.items():
            _imports += f"from {_from} import {', '.join(_import)}\n"

        _py = _imports + "\n\n" + _py

    with open(path, "w") as f:
        f.write(_py)
        f.write("\n")


def handle_renovation_controller(doc, r_dt_folder):
    target_file = os.path.join(r_dt_folder, renovation.scrub(doc.name) + ".py")
    if os.path.exists(target_file):
        return

    dt_title_case = doc.name.replace(' ', '')
    py_content = f"""
from renovation import RenovationModel
from .{renovation.scrub(doc.name)}_types import {dt_title_case}Meta


class {dt_title_case}(RenovationModel["{dt_title_case}"], {dt_title_case}Meta):
    pass
"""

    with open(target_file, "w") as f:
        f.write(py_content)


def handle_frappe_controller(doc, r_dt_module):
    from frappe.model.document import get_controller
    target_file = renovation.get_module(get_controller(doc.name).__module__).__file__
    with open(target_file, "r") as f:
        file_content = f.read()

    dt_title = doc.name.replace(" ", "")
    if f"class {dt_title}(_{dt_title}):" in file_content:
        # Assume all good
        return

    file_content = file_content.replace(
        "from frappe.model.document import Document",
        f"""from renovation.model import map_doctype
from {r_dt_module} import {dt_title} as _{dt_title}""")

    file_content = file_content.replace(
        f"class {dt_title}(Document):",
        f"""map_doctype("{doc.name}", _{dt_title})


class {dt_title}(_{dt_title}):"""
    )

    with open(target_file, "w") as f:
        f.write(file_content)
