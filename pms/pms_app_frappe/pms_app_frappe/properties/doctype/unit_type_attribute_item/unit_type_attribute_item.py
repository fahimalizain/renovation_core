# Copyright (c) 2021, Leam Technology Systems and contributors
# For license information, please see license.txt

from renovation.model import map_doctype
from pms_app.properties.models.unit_type_attribute_item import (
    UnitTypeAttributeItem as _UnitTypeAttributeItem)

map_doctype("Unit Type Attribute Item", _UnitTypeAttributeItem)


class UnitTypeAttributeItem(_UnitTypeAttributeItem):
    pass
