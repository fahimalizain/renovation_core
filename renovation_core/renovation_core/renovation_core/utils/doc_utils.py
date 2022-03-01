
from typing import List

import frappe
from frappe.core.doctype.version.version import get_diff


def has_table_value_changed(doc, table_name) -> List[dict]:
    """Checks if there has been any changes in a table on a doc"""

    changes = frappe._dict()

    if not doc.get("_doc_before_save"):
        return changes

    diff = get_diff(doc.get("_doc_before_save"), doc)

    if not diff:
        return changes

    added_rows = [
        added[1] for added in diff.get("added") if added[0] == table_name
    ]

    if added_rows:
        changes.update({"added": added_rows})

    removed_rows = [
        removed[1]
        for removed in diff.get("removed")
        if removed[0] == table_name
    ]

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
