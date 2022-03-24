# Copyright (c) 2022, Leam Technology Systems and contributors
# For license information, please see license.txt

# import frappe
from renovation.model import map_doctype
from pms_app.pms_core.models.pms_custom_field_value.pms_custom_field_value import \
    PMSCustomFieldValue as _PMSCustomFieldValue

map_doctype("PMS Custom Field Value", _PMSCustomFieldValue)


class PMSCustomFieldValue(_PMSCustomFieldValue):
    pass
