# Copyright (c) 2021, Leam Technology Systems and contributors
# For license information, please see license.txt

from renovation.model import map_doctype
from pms_app.properties.models.unit import Unit as _Unit

map_doctype("Unit", _Unit)


class Unit(_Unit):
    pass
