# Copyright (c) 2022, Leam Technology Systems and contributors
# For license information, please see license.txt

from renovation.model import map_doctype
from pms_app.properties.models.property_type.property_type import PropertyType as _PropertyType


map_doctype("Property Type", _PropertyType)


class PropertyType(_PropertyType):
    pass
