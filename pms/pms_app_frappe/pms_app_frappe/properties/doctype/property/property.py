# Copyright (c) 2022, Leam Technology Systems and contributors
# For license information, please see license.txt

from renovation.model import map_doctype
from pms_app.properties.models.property import Property as _Property


map_doctype("Property", _Property)


class Property(_Property):
    pass
