# Copyright (c) 2021, Leam Technology Systems and contributors
# For license information, please see license.txt

# import frappe
# from frappe import _
from frappe.model.document import Document
# from pms_app.properties.exceptions import UnitAttributeError
# from pms_app.utils.numbers import is_number


class UnitAttributeItem(Document):
    pass
    # def validate_unit_attribute_on_linked_unit_type(self, parent):
    #     """Validate that all attributes exist on the liked Unit Type"""

    #     unit_type = frappe.get_doc("Unit Type", parent.unit_type)

    #     allowed_attributes = [doc.name for doc in frappe.get_all(
    #         "Unit Type Attribute Item",
    #         filters=[["parent", "=", unit_type.name]]
    #     )]

    #     if self.attribute_link not in allowed_attributes:

    #         frappe.throw(
    #             _(
    #                 "Error in Unit Attributes No.{0}: '{1}' "
    #                 "does not exist on the linked Unit Type"
    #             )
    #             .format(self.idx, self.title),
    #             UnitAttributeError
    #         )

    # def validate_unit_attribute_value_type(self):
    #     if self.attribute_type in ["Data", "Number", "Select"]:

    #         # No new-line except in Multi_Select
    #         if "\n" in self.value:
    #             frappe.throw(
    #                 _(
    #                     "Error in Unit Attributes No.{0}: '{1}' "
    #                     "Cannot have more than one option (seperated by newline) "
    #                     "in Value if type is not Multi-Select"
    #                 )
    #                 .format(self.idx, self.title),
    #                 UnitAttributeError
    #             )

    #         # No non-numeric value
    #         if self.attribute_type == "Number" and not is_number(self.value):
    #             frappe.throw(
    #                 _(
    #                     "Error in Unit Attributes No.{0}: '{1}' "
    #                     "Field of type Number cannot have non-numeric Value"
    #                 )
    #                 .format(self.idx, self.title),
    #                 UnitAttributeError
    #             )

    #         # Check that value is in options
    #         if self.attribute_type == "Select":
    #             if self.value not in self.select_options.split("\n"):
    #                 frappe.throw(
    #                     _(
    #                         "Error in Unit Attributes No.{0}: '{1}' "
    #                         "Value not in Select Options"
    #                     )
    #                     .format(self.idx, self.title),
    #                     UnitAttributeError
    #                 )

    #     elif self.attribute_type == "Multi-Select":

    #         for option in self.value.split("\n"):
    #             if option not in self.select_options.split("\n"):
    #                 if option not in self.select_options.split("\n"):
    #                     frappe.throw(
    #                         _(
    #                             "Error in Unit Attributes No.{0}: '{1}' "
    #                             "One or more Value not in Select Options"
    #                         )
    #                         .format(self.idx, self.title),
    #                         UnitAttributeError
    #                     )
