# Copyright (c) 2022, Leam Technology Systems and contributors
# For license information, please see license.txt

# import frappe
from renovation.model import map_doctype
from pms_app.pms_core.models.pms_custom_field.pms_custom_field import \
    PMSCustomField as _PMSCustomField

map_doctype("PMS Custom Field", _PMSCustomField)


class PMSCustomField(_PMSCustomField):
    pass
