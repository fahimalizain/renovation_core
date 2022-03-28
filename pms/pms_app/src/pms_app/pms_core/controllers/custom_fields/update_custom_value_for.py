from functools import reduce
from asyncer import asyncify

import renovation
from pms_app.utils import NotFound, PermissionDenied
from pms_app.pms_core.models.pms_custom_field_value.pms_custom_field_value import \
    PMSCustomFieldValue
from .get_custom_field_values_for import get_custom_field_values_for


async def update_custom_values_for(entity_type: str, entity: str, values: dict):

    if not renovation.local.db.exists(entity_type, entity):
        raise NotFound(message=renovation._("Entity Not Found: {0} {1}").format(
            entity_type, entity), entity_type=entity_type, entity=entity)

    if not renovation.has_permission(entity_type, doc=entity, ptype="read"):
        raise PermissionDenied(
            message=renovation._("You do not have permission on {0} {1}").format(
                entity_type, entity))

    _sql = asyncify(renovation.local.db.sql)

    # Get existing values first
    existing_values = await _sql("""
    SELECT
        cf_value.*
    FROM `tabPMS Custom Field Value` cf_value
    JOIN `tabPMS Custom Field` cf ON cf.fieldname = cf_value.fieldname
    WHERE
        cf_value.entity_type = %(entity_type)s
        AND cf_value.entity = %(entity)s
    """, dict(entity_type=entity_type, entity=entity), as_dict=1)

    _values = reduce(
        lambda r, cf_value: (r.update({cf_value.fieldname: PMSCustomFieldValue(cf_value)}) or r),
        existing_values, renovation._dict()
    )

    for fieldname, value in values.items():
        if fieldname not in _values:
            _values[fieldname] = PMSCustomFieldValue(dict(
                fieldname=fieldname,
                entity_type=entity_type, entity=entity
            ))

        _values[fieldname].value = value
        await _values[fieldname].save(ignore_permissions=True)

    return get_custom_field_values_for(entity_type=entity_type, entity=entity)
