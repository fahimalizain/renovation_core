from asyncer import asyncify

import renovation
from pms_app.pms_core.models.pms_custom_field_value.pms_custom_field_value import get_parsed_value
from pms_app.utils.exceptions import PermissionDenied, NotFound


async def get_custom_field_values_for(entity_type: str, entity: str):
    """
    Gets the Custom Field Values after parsing them to their proper formats
    """

    if not renovation.local.db.exists(entity_type, entity):
        raise NotFound(message=renovation._("Entity Not Found: {0} {1}").format(
            entity_type, entity), entity_type=entity_type, entity=entity)

    if not renovation.has_permission(entity_type, doc=entity, ptype="read"):
        raise PermissionDenied(
            message=renovation._("You do not have permission on {0} {1}").format(
                entity_type, entity))

    _sql = asyncify(renovation.local.db.sql)
    r = await _sql("""
    SELECT
        cf_value.fieldname, cf_value.value, cf.fieldtype, cf.options
    FROM `tabPMS Custom Field Value` cf_value
    JOIN `tabPMS Custom Field` cf ON cf_value.fieldname = cf.fieldname
    WHERE
        cf_value.entity_type = %(entity_type)s
        AND cf_value.entity = %(entity)s
    """, dict(entity_type=entity_type, entity=entity), as_dict=1, debug=0)

    result = renovation._dict()
    for cf_value in r:
        result[cf_value.fieldname] = await get_parsed_value(
            value=cf_value.value, fieldtype=cf_value.fieldtype, options=cf_value.options)

    return result
