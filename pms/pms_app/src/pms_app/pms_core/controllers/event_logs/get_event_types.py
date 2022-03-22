# from functools import reduce
from asyncer import asyncify

import renovation
from pms_app.pms_core.models.event_type.event_type import EventType  # noqa


async def get_event_types(model: str):

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

    # role_event_types = [x[0] for x in (await _sql("""
    # SELECT
    #     parent as event_type
    # FROM `tabHas Role` WHERE
    #     parenttype = "Event Type"
    #     AND role IN %(roles)s
    # """, dict(roles=frappe.get_roles())))]

    # model_event_types = await _sql("""
    # SELECT parent as event_type, model
    # FROM `tabModel Selector`
    # WHERE
    #     parenttype = "Event Type"
    #     AND parent = %(event_types)s
    # """, dict(
    #     event_types=role_event_types,
    # ), as_dict=1)

    # _event_type_model_map = reduce(
    #     lambda d, e: (d.setdefault(e.event_type, []).append(e.model) or d),
    #     model_event_types, renovation._dict())

    # _event_types = []
    # for event_type, models in _event_type_model_map.items():
    #     if model not in models:
    #         continue
    #     _event_types.append(event_type)

    # _event_types = await _sql("""
    # SELECT name, title, actions, action_info
    # FROM `tabEvent Type` WHERE name IN %(event_types)s
    # """, dict(event_types=_event_types), as_dict=1)

    return event_types
