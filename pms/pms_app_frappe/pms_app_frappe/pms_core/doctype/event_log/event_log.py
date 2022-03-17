# Copyright (c) 2022, Leam Technology Systems and contributors
# For license information, please see license.txt

# import frappe
from renovation.model import map_doctype
from pms_app.pms_core.models.event_log.event_log import EventLog as _EventLog

map_doctype("Event Log", _EventLog)


class EventLog(_EventLog):
    pass
