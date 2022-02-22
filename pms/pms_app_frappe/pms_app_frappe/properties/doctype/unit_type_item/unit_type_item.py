# Copyright (c) 2022, Leam Technology Systems and contributors
# For license information, please see license.txt

# import frappe
# from frappe import _
from frappe.model.document import Document
# from pms_app.properties.exceptions import UnitTypeNotFound


class UnitTypeItem(Document):
    pass
    # def validate_unit_type_enabled(self):

    #     if not frappe.get_value("Unit Type", self.unit_type, "enabled"):

    #         frappe.throw(
    #             _(
    #                 "Disabled Unit Type found in Unit Types No. {0}: '{1}'"
    #             ).format(self.idx, self.unit_type),
    #             UnitTypeNotFound
    #         )
