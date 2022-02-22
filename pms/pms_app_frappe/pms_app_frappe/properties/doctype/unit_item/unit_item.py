# Copyright (c) 2022, Leam Technology Systems and contributors
# For license information, please see license.txt

from renovation.model import map_doctype
from pms_app.properties.models.unit_item import UnitItem as _UnitItem


map_doctype("Unit Item", _UnitItem)


class UnitItem(_UnitItem):
    pass
