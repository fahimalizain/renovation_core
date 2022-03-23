from asyncer import asyncify
from pms_app.pms_core.models.event_log.event_log import EventLog

import renovation
from pms_app.utils.exceptions import PermissionDenied, NotFound


async def get_event_thread(parent_log: str = None):
    """
    Gets all Primary EventLogs of EventThreads
    """
    if not await EventLog.exists(parent_log):
        raise NotFound(message=renovation._("Event Log not found"), event_log=parent_log)

    # Verify read perms on specified document
    entity_type, entity = await EventLog.db_get_value(parent_log, ["entity_type", "entity"])
    if not renovation.has_permission(doctype=entity_type, doc=entity, ptype="read"):
        raise PermissionDenied(
            renovation._(f"You do not have access to {entity_type}: {entity}"),
            model=entity_type,
            name=entity)

    _sql = asyncify(renovation.local.db.sql)
    t = await _sql("""
        SELECT
            event_log.name, event_log.parent_log,
            event_log.entity_type, event_log.entity,
            event_log.created_by, event_log.event_type,
            event_log.attachment, event_log.content,
            event_log.ref_dt, event_log.ref_dn
        FROM
            `tabEvent Log` event_log
        WHERE
            event_log.name = %(parent_log)s OR event_log.parent_log = %(parent_log)s
        ORDER BY
            creation asc
    """, dict(parent_log=parent_log), as_dict=1)

    return t
