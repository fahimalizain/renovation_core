# Copyright (c) 2021, Leam Technology Systems and contributors
# For license information, please see license.txt

# import frappe
# from frappe import _
from frappe.model.document import Document
# from pms_app.properties.exceptions import UnitAttributeError
# from pms_app.utils.numbers import is_number


class UnitTypeAttributeItem(Document):
    pass
    # def validate_select_options(self):
    #     """Validate Select Options for the attribute"""

    #     if self.attribute_type in ["Select", "Multi-Select"]:

    #         # One or more select options
    #         if not self.select_options:
    #             frappe.throw(_(
    #                 "Cannot set Attribute Type No.{0} '{1}' as a Select or Multi-Select"
    #                 " field without specifying at least one option.")
    #                 .format(self.idx, self.title),
    #                 UnitAttributeError
    #             )

    #         # Duplicates in options
    #         options = self.select_options.split("\n")
    #         if len(options) != len(set(options)):
    #             frappe.throw(
    #                 _(
    #                     "Error in Unit Attributes No.{0}: '{1}' "
    #                     "Select Options cannot have duplicates"
    #                 )
    #                 .format(self.idx, self.title),
    #                 UnitAttributeError
    #             )

    # def validate_default_value(self):
    #     """Validate Default Value for the attribute"""

    #     if self.attribute_type in ["Data", "Number", "Select"]:

    #         # No new-line except in Multi_Select
    #         if "\n" in self.default_value:
    #             frappe.throw(
    #                 _(
    #                     "Error in Unit Attributes No.{0}: '{1}' "
    #                     "Cannot have more than one option (seperated by newline) "
    #                     "if type is not Multi-Select"
    #                 )
    #                 .format(self.idx, self.title),
    #                 UnitAttributeError
    #             )

    #         # No non-numeric value
    #         if self.attribute_type == "Number" and not is_number(self.default_value):
    #             frappe.throw(
    #                 _(
    #                     "Error in Unit Attributes No.{0}: '{1}' "
    #                     "Field of type Number cannot have non-numeric Default Value"
    #                 )
    #                 .format(self.idx, self.title),
    #                 UnitAttributeError
    #             )

    #         # Check that default value is in options
    #         if self.attribute_type == "Select":
    #             if self.default_value not in self.select_options.split("\n"):
    #                 frappe.throw(
    #                     _(
    #                         "Error in Unit Attributes No.{0}: '{1}' "
    #                         "Default Value not in Select Options"
    #                     )
    #                     .format(self.idx, self.title),
    #                     UnitAttributeError
    #                 )

    #     elif self.attribute_type == "Multi-Select":

    #         for option in self.default_value.split("\n"):
    #             if option not in self.select_options.split("\n"):
    #                 frappe.throw(
    #                     _(
    #                         "Error in Unit Attributes No.{0}: '{1}' "
    #                         "One or more Default Value not in Select Options"
    #                     )
    #                     .format(self.idx, self.title),
    #                     UnitAttributeError
    #                 )
