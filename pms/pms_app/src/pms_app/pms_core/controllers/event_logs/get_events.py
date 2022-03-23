from asyncer import asyncify

import renovation
from pms_app.utils.exceptions import PermissionDenied


async def get_events(model: str, name: str):
    """
    Gets all Primary EventLogs of EventThreads
    """
    # Verify read perms on specified document
    if not renovation.has_permission(doctype=model, doc=name, ptype="read"):
        raise PermissionDenied(
            renovation._(f"You do not have access to {model}: {name}"),
            model=model,
            name=name)

    _sql = asyncify(renovation.local.db.sql)
    t = await _sql("""
    SELECT
        event_log.entity_type, event_log.entity,
        coalesce(primary_log.created_by, event_log.created_by) AS created_by,
        coalesce(primary_log.event_type, event_log.event_type) AS event_type,
        coalesce(primary_log.ref_dt, event_log.ref_dt) AS ref_dt,
        coalesce(primary_log.ref_dn, event_log.ref_dn) AS ref_dn,
        coalesce(primary_log.attachment, event_log.attachment) AS attachment,
        coalesce(primary_log.content, event_log.content) AS content
    FROM `tabEvent Log` event_log
    LEFT JOIN `tabEvent Log` primary_log ON event_log.primary_log = primary_log.name
    WHERE
        event_log.entity_type = %(model)s
        AND event_log.entity = %(name)s
        AND event_log.parent_log IS NULL
    """, dict(model=model, name=name), as_dict=1)

    return t
