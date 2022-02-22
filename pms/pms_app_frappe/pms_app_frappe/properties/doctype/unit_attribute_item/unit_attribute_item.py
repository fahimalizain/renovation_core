# Copyright (c) 2021, Leam Technology Systems and contributors
# For license information, please see license.txt

from renovation.model import map_doctype
from pms_app.properties.models.unit_attribute_item import UnitAttributeItem as _UnitAttributeItem


map_doctype("Unit Attribute Item", _UnitAttributeItem)


class UnitAttributeItem(_UnitAttributeItem):
    pass
