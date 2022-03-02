
from renovation import RenovationModel, _
from pms_app.properties.exceptions import UnitAttributeError
from pms_app.utils.numbers import is_number

from .unit_type_attribute_item_types import UnitTypeAttributeItemMeta


class UnitTypeAttributeItem(RenovationModel["UnitTypeAttributeItem"], UnitTypeAttributeItemMeta):
    def validate_select_options(self):
        """Validate Select Options for the attribute"""

        if self.attribute_type in ["Select", "Multi-Select"]:

            # One or more select options
            if not self.select_options:
                raise UnitAttributeError(_(
                    "Cannot set Attribute Type No.{0} '{1}' as a Select or Multi-Select"
                    " field without specifying at least one option.")
                    .format(self.idx, self.title)
                )

            # Duplicates in options
            options = self.select_options.split("\n")
            if len(options) != len(set(options)):
                raise UnitAttributeError(
                    _(
                        "Error in Unit Attributes No.{0}: '{1}' "
                        "Select Options cannot have duplicates"
                    )
                    .format(self.idx, self.title),
                )

    def validate_default_value(self):
        """Validate Default Value for the attribute"""

        if self.attribute_type in ["Data", "Number", "Select"]:

            # No new-line except in Multi_Select
            if "\n" in self.default_value:
                raise UnitAttributeError(
                    _(
                        "Error in Unit Attributes No.{0}: '{1}' "
                        "Cannot have more than one option (seperated by newline) "
                        "if type is not Multi-Select"
                    )
                    .format(self.idx, self.title),
                )

            # No non-numeric value
            if self.attribute_type == "Number" and not is_number(self.default_value):
                raise UnitAttributeError(
                    _(
                        "Error in Unit Attributes No.{0}: '{1}' "
                        "Field of type Number cannot have non-numeric Default Value"
                    )
                    .format(self.idx, self.title),
                )

            # Check that default value is in options
            if self.attribute_type == "Select":
                if self.default_value not in self.select_options.split("\n"):
                    raise UnitAttributeError(
                        _(
                            "Error in Unit Attributes No.{0}: '{1}' "
                            "Default Value not in Select Options"
                        )
                        .format(self.idx, self.title),
                    )

        elif self.attribute_type == "Multi-Select":

            for option in self.default_value.split("\n"):
                if option not in self.select_options.split("\n"):
                    raise UnitAttributeError(
                        _(
                            "Error in Unit Attributes No.{0}: '{1}' "
                            "One or more Default Value not in Select Options"
                        )
                        .format(self.idx, self.title),
                    )
