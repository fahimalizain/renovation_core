from asyncer import asyncify
import frappe

from pms_app.pms_core.controllers.custom_fields import (
    get_custom_fields, update_custom_values_for, get_custom_field_values_for)


async def on_update(doc, method=None):
    fields = await get_custom_fields(entity_type=doc.doctype, entity=doc.name)
    if not len(fields):
        return

    _values = dict()
    for df in fields:
        if not doc.get(df.fieldname):
            continue
        _values[df.fieldname] = doc.get(df.fieldname)

    await update_custom_values_for(
        entity_type=doc.doctype, entity=doc.name, values=_values
    )


async def onload(doc, method=None):
    values = await get_custom_field_values_for(
        entity_type=doc.doctype, entity=doc.name
    )
    if values:
        doc.update(values)


async def on_trash(doc, method=None):
    await asyncify(frappe.db.sql)("""
    DELETE FROM `tabPMS Custom Field Value` WHERE
        entity_type = %(entity_type)s
        AND entity = %(entity)s
    """, dict(entity_type=doc.doctype, entity=doc.name))
