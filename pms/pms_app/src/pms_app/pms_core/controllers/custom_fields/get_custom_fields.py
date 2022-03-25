from asyncer import asyncify

import renovation
from pms_app.utils.exceptions import InvalidArguments, PermissionDenied


async def get_custom_fields(entity_type: str = None, entity: str = None):
    if "Sys Admin" not in renovation.get_roles():
        raise PermissionDenied(message=renovation._(
            "Only users with role 'Sys Admin' can perform this action"))

    if entity and not entity_type:
        raise InvalidArguments(
            message=renovation._("Please mention entity_type when specifying entity"),
            entity=entity
        )

    _sql = asyncify(renovation.local.db.sql)

    conditions = []

    if entity_type:
        conditions.append("(cf.entity_type = %(entity_type)s OR cf.entity_type IS NULL)")

        # Consider cf.excluded_entities for Global Custom Fields
        conditions.append(
            "(excluded_entity.model IS NULL OR excluded_entity.model != %(entity_type)s)")

    if entity:
        conditions.append("(cf.entity = %(entity)s OR cf.entity IS NULL)")

    r = await _sql("""
    SELECT
        cf.name, enabled, label, fieldname, fieldtype, options, description,
        insert_after, entity, entity_type, cf.creation,
        GROUP_CONCAT(DISTINCT excluded_entity.model SEPARATOR ', ') AS entities_excluded
    FROM `tabPMS Custom Field` cf
    LEFT JOIN `tabModel Selector` excluded_entity
        ON excluded_entity.parent = cf.name AND excluded_entity.parenttype = "PMS Custom Field"
    {conditions}
    GROUP BY cf.name
    ORDER BY cf.creation desc
    """.format(
        conditions="WHERE {}".format(" AND ".join(conditions)) if len(conditions) else ""
    ), dict(
        entity=entity, entity_type=entity_type
    ), as_dict=1)

    for cf in r:
        if not cf.entities_excluded:
            cf.entities_excluded = []
        else:
            cf.entities_excluded = cf.entities_excluded.split(", ")

    return r
