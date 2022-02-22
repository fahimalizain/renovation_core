from typing import Union
from collections.abc import MutableSequence, MutableMapping

import frappe
from frappe.model import default_fields
from frappe.model.base_document import BaseDocument
from frappe.core.doctype.version.version import get_diff


def strip_default_fields(doc: Union[BaseDocument, dict]):
    if isinstance(doc, BaseDocument):
        doc = doc.as_dict()

    doc = {
        k: v if not isinstance(v, list) else [strip_default_fields(x) for x in v]
        for k, v in doc.items() if k == "name" or k not in default_fields
    }

    return dictify(doc)


def dictify(arg):
    if isinstance(arg, MutableSequence):
        for i, a in enumerate(arg):
            arg[i] = dictify(a)
    elif isinstance(arg, MutableMapping):
        arg = frappe._dict(arg)
        for k in arg.keys():
            arg[k] = dictify(arg[k])

    return arg


def has_table_value_changed(doc, table_name):
    """Checks if there has been any changes in a table on a doc, returns changes"""

    changes = frappe._dict()

    if not doc.get("_doc_before_save"):
        return changes

    diff = get_diff(doc.get("_doc_before_save"), doc)

    if not diff:
        return changes

    added_rows = []
    for added in diff.get("added"):
        if added[0] == table_name:
            added_rows.append(added[1])
    if added_rows:
        changes.update({"added": added_rows})

    removed_rows = []
    for removed in diff.get("removed"):
        if removed[0] == table_name:
            removed_rows.append(removed[1])
    if removed_rows:
        changes.update({"removed": removed_rows})

    updated_rows = []
    for row in diff.get("row_changed"):
        if row[0] == table_name:

            # Update doesn't provide the row (just changes) so fetch it
            whole_row = [
                item for item in doc.get("_doc_before_save").get(table_name)
                if item.name == row[2]
            ]

            updated_rows.append({
                "idx": row[1],
                "name": row[2],
                "changes": row[3],
                "row": whole_row[0] if whole_row else None,
            })
    if updated_rows:
        changes.update({"updated": updated_rows})

    return changes
