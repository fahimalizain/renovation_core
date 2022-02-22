# Copyright (c) 2022, Leam Technology Systems and contributors
# For license information, please see license.txt

# import frappe
# from frappe import _
from frappe.model.document import Document
# from pms_app.properties.exceptions import PropertyTypeNotEnabled, UnitError, UnitItemError


class Property(Document):
    pass
    # def validate(self):

    #     self.validate_property_type()
    #     self.validate_units()

    # def validate_units(self):

    #     for unit in self.units:
    #         self.validate_unique_unit(unit)
    #         self.validate_unit_type_of_unit(unit)

    # def validate_property_type(self):
    #     """Validate that if self is active, only enabled Property Types can be added"""

    #     if self.active:
    #         property_type_enabled = frappe.get_value("Property Type", self.property_type, "enabled")
    #         if not property_type_enabled:

    #             frappe.throw(
    #                 _(
    #                     "A disabled Property Type cannot be added to an active Property"
    #                 ),
    #                 PropertyTypeNotEnabled
    #             )

    # def validate_unique_unit(self, unit_item):
    #     """Validate that a Unit can only exist on one Property"""

    #     unit_items = frappe.get_all(
    #         "Unit Item",
    #         filters=[
    #             ["unit", "=", unit_item.unit],
    #             ["parent", "!=", self.name]
    #         ],
    #         fields=["parent"]
    #     )

    #     if unit_items:
    #         frappe.throw(
    #             _(
    #                 "Error adding Unit No. {0}. '{1}'. This Unit already exists on Property '{2}'"
    #             ).format(unit_item.idx, unit_item.unit, unit_items[0].parent),
    #             UnitError
    #         )

    # def validate_unit_type_of_unit(self, unit_item):
    #     """Validate that only Units with Unit Types that exist on the Property Type are allowed"""

    #     property_type_doc = frappe.get_doc("Property Type", self.property_type)

    #     supported_unit_types = set([
    #         unit_type_item.unit_type for unit_type_item in property_type_doc.unit_types
    #     ])

    #     for unit_item in self.units:
    #         if unit_item.unit_type not in supported_unit_types:
    #             frappe.throw(
    #                 _(
    #                     "Unit No. {0}: '{1}' has a Unit Type of '{2}' which is not "
    #                     "supported by Property Type '{3}'"
    #                 ).format(
    #                     unit_item.idx, unit_item.unit, unit_item.unit_type, self.property_type
    #                 ),
    #                 UnitItemError
    #             )
