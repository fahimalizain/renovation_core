# Copyright (c) 2022, Leam Technology Systems and contributors
# For license information, please see license.txt

# import frappe
from renovation.model import map_doctype
from pms_app.pms_core.models.event_type.event_type import EventType as _EventType

map_doctype("Event Type", _EventType)


class EventType(_EventType):
    pass
