# from functools import reduce
from asyncer import asyncify

import renovation
from pms_app.pms_core.models.event_type.event_type import EventType  # noqa


async def get_event_types(model: str):
    """
    Gets a list of event types
    """

    # EventTypes with empty roles means nobody can create it directly
    # EventTypes with empty models would mean it can be applied to any Model

    # Fetch all the EventTypes supported by this User
    import frappe
    _sql = asyncify(renovation.local.db.sql)

    roles = frappe.get_roles()
    event_types = await _sql("""
    SELECT DISTINCT
        event_type.name, event_type.title, event_type.actions, event_type.action_info
    FROM `tabEvent Type` event_type
    JOIN `tabHas Role` has_role
        ON has_role.parent = event_type.name AND has_role.parenttype = "Event Type"
    LEFT JOIN `tabModel Selector` model_selector
        ON model_selector.parent = event_type.name AND model_selector.parenttype = "Event Type"
    WHERE
        has_role.role IN %(roles)s
        AND (model_selector.model IS NULL OR model_selector.model = %(model)s)
    """, dict(roles=roles, model=model), as_dict=1, debug=0)

    return event_types
