# Copyright (c) 2022, Leam Technology Systems and contributors
# For license information, please see license.txt

from renovation.model import map_doctype
# from pms_app.properties.exceptions import UnitTypeNotFound
from pms_app.properties.models.unit_type_item import UnitTypeItem as _UnitTypeItem

map_doctype("Unit Type Item", _UnitTypeItem)


class UnitTypeItem(_UnitTypeItem):
    pass
    # def validate_unit_type_enabled(self):

    #     if not frappe.get_value("Unit Type", self.unit_type, "enabled"):

    #         frappe.throw(
    #             _(
    #                 "Disabled Unit Type found in Unit Types No. {0}: '{1}'"
    #             ).format(self.idx, self.unit_type),
    #             UnitTypeNotFound
    #         )
