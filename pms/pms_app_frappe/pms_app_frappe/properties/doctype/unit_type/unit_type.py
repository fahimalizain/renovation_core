# Copyright (c) 2021, Leam Technology Systems and contributors
# For license information, please see license.txt

# import frappe
# from frappe import _
# from frappe.model.document import Document
# from pms_app.properties.exceptions import UnitAttributeError
# from pms_app.utils.doc_utils import has_table_value_changed
from renovation.model import map_doctype
from pms_app.properties.models.unit_type import UnitType as _UnitType


map_doctype("Unit Type", _UnitType)


class UnitType(_UnitType):
    pass
