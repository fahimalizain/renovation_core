# Copyright (c) 2021, Leam Technology Systems and contributors
# For license information, please see license.txt

# import frappe
# from frappe import _
from frappe.model.document import Document
# from pms_app.properties.exceptions import UnitTypeNotFound


class Unit(Document):
    pass
    # def before_insert(self):
    #     self.copy_attributes_from_unit_type()

    # def validate(self):

    #     self.validate_enabled_unit_type()
    #     if self.flags.in_insert:
    #         self.validate_unit_attributes()  # For save(), validate separately

    # def on_change(self):

    #     if self.has_value_changed("unit_type"):
    #         self.update_property_unit_items()

    #     # If not in insert, copy the attributes from the Unit Type
    #     # Set a flag before the save and reset it after to avoid recursive save() calls

    #     if not self.flags.in_insert and not self.flags.saving_attributes:
    #         self.flags.saving_attributes = True

    #         self.copy_attributes_from_unit_type(set_name=True)
    #         self.validate_unit_attributes()  # Run previously ignored validation
    #         self.save()

    #     if self.flags.saving_attributes:
    #         self.flags.saving_attributes = False

    # def copy_attributes_from_unit_type(self, set_name=False):

    #     updated_attributes = []

    #     unit_type = frappe.get_doc("Unit Type", self.unit_type)
    #     for type_attribute in unit_type.unit_attributes:

    #         existing_row = [
    #             attribute_row for attribute_row in self.unit_attributes
    #             if attribute_row.attribute_link == type_attribute.name
    #         ]

    #         if existing_row:
    #             existing_row = existing_row[0]
    #             existing_row.title = type_attribute.title
    #             existing_row.attribute_type = type_attribute.attribute_type
    #             existing_row.select_options = type_attribute.select_options
    #             updated_attributes.append(existing_row)
    #         else:
    #             new_row = frappe.get_doc({
    #                 "doctype": "Unit Attribute Item",
    #                 "parenttype": self.doctype,
    #                 "parent": self.name if set_name else None,
    #                 "parentfield": "unit_attributes",
    #                 "title": type_attribute.title,
    #                 "attribute_type": type_attribute.attribute_type,
    #                 "value": type_attribute.default_value,
    #                 "attribute_link": type_attribute.name,
    #                 "select_options": type_attribute.select_options
    #             })

    #             updated_attributes.append(new_row)

    #     self.update({"unit_attributes": updated_attributes})

    # def validate_enabled_unit_type(self):
    #     """Validate that only an enabled Unit Type can be added, if self is set to active"""

    #     unit_type = frappe.get_doc("Unit Type", self.unit_type)

    #     if not unit_type.enabled and self.active:
    #         frappe.throw(
    #             _(
    #                 "The linked Unit Type '{0}' is not enabled"
    #             ).format(unit_type.name),
    #             UnitTypeNotFound
    #         )

    # def validate_unit_attributes(self):
    #     """Validate the list of Unit Attributes"""

    #     for attribute in self.unit_attributes:
    #         attribute.validate_unit_attribute_on_linked_unit_type(self)
    #         attribute.validate_unit_attribute_value_type()

    # def update_property_unit_items(self):
    #     """Update the Unit Items on Properties containing this Unit"""

    #     linked_unit_items = frappe.get_all(
    #         "Unit Item",
    #         filters=[["unit", "=", self.name]]
    #     )

    #     for linked_unit_item in linked_unit_items:
    #         frappe.db.set_value("Unit Item", linked_unit_item.name, "unit_type", self.unit_type)
