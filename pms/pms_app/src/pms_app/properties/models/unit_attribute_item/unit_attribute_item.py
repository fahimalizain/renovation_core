
from renovation import RenovationModel, _

from pms_app.properties.exceptions import UnitAttributeError
from pms_app.utils.numbers import is_number

from ..unit_type.unit_type import UnitType
from ..unit_type_attribute_item.unit_type_attribute_item import UnitTypeAttributeItem

from .unit_attribute_item_types import UnitAttributeItemMeta


class UnitAttributeItem(RenovationModel["UnitAttributeItem"], UnitAttributeItemMeta):
    async def validate_unit_attribute_on_linked_unit_type(self, parent):
        """Validate that all attributes exist on the liked Unit Type"""

        unit_type = await UnitType.get_doc(parent.unit_type)

        allowed_attributes = [doc.name for doc in await UnitTypeAttributeItem.get_all(
            filters=[["parent", "=", unit_type.name]])]

        if self.attribute_link not in allowed_attributes:

            raise UnitAttributeError(
                _(
                    "Error in Unit Attributes No.{0}: '{1}' "
                    "does not exist on the linked Unit Type"
                )
                .format(self.idx, self.title)
            )

    def validate_unit_attribute_value_type(self):
        if self.attribute_type in ["Data", "Number", "Select"]:

            # No new-line except in Multi_Select
            if "\n" in self.value:
                raise UnitAttributeError(
                    _(
                        "Error in Unit Attributes No.{0}: '{1}' "
                        "Cannot have more than one option (seperated by newline) "
                        "in Value if type is not Multi-Select"
                    )
                    .format(self.idx, self.title)
                )

            # No non-numeric value
            if self.attribute_type == "Number" and not is_number(self.value):
                raise UnitAttributeError(
                    _(
                        "Error in Unit Attributes No.{0}: '{1}' "
                        "Field of type Number cannot have non-numeric Value"
                    )
                    .format(self.idx, self.title)
                )

            # Check that value is in options
            if self.attribute_type == "Select":
                if self.value not in self.select_options.split("\n"):
                    raise UnitAttributeError(
                        _(
                            "Error in Unit Attributes No.{0}: '{1}' "
                            "Value not in Select Options"
                        )
                        .format(self.idx, self.title)
                    )

        elif self.attribute_type == "Multi-Select":

            for option in self.value.split("\n"):
                if option not in self.select_options.split("\n"):
                    if option not in self.select_options.split("\n"):
                        raise UnitAttributeError(
                            _(
                                "Error in Unit Attributes No.{0}: '{1}' "
                                "One or more Value not in Select Options"
                            )
                            .format(self.idx, self.title)
                        )
