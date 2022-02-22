from renovation import RenovationModel, _
from pms_app.properties.exceptions import UnitAttributeError


class UnitType(RenovationModel["UnitType"]):
    def validate(self):
        self.validate_unit_attributes()

    # def on_change(self):

    #     if self.has_value_changed("enabled") and not self.enabled:
    #         self.set_linked_units_deactivated()

    #     self.propagate_changes_to_linked_unit_instances()

    def validate_unit_attributes(self):
        """Validate the table of Unit Attributes"""

        unit_attribute_titles = [unit_attribute.title for unit_attribute in self.unit_attributes]

        if len(unit_attribute_titles) != len(set(unit_attribute_titles)):
            raise UnitAttributeError(_(
                "Unit Attribute titles must be unique"
            )
                .format(self.idx, self.title))

        for attribute in self.unit_attributes:
            attribute.validate_select_options()
            attribute.validate_default_value()

    # def set_linked_units_deactivated(self):
    #     """Set all Units linked to deactivated"""

    #     linked_units = frappe.get_all(
    #         "Unit",
    #         filters=[["unit_type", "=", self.name]]
    #     )

    #     for unit in linked_units:
    #         frappe.set_value("Unit", unit.name, "active", 0)

    # def propagate_changes_to_linked_unit_instances(self):

    #     changes = has_table_value_changed(self, "unit_attributes")
    #     if changes:

    #         linked_units = frappe.get_all(
    #             "Unit",
    #             filters=[["unit_type", "=", self.name]]
    #         )

    #         for unit in linked_units:
    #             doc = frappe.get_doc("Unit", unit.name)

    #             if changes.get("removed"):
    #                 for update in changes.get("removed"):

    #                     doc.unit_attributes = [
    #                         attribute for attribute in doc.unit_attributes
    #                         if attribute.attribute_link != update.get("name")
    #                     ]

    #             if changes.get("updated"):
    #                 for update in changes.get("updated"):
    #                     # if the attribute has been changed, remove it from the linked Unit
    #                     # The Unit controller will take care of copying it over again
    #                     doc.unit_attributes = [
    #                         attribute for attribute in doc.unit_attributes
    #                         if attribute.attribute_link != update.get("name")
    #                     ]
    #             doc.save()
