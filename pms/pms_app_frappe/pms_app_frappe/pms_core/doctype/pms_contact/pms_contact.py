# Copyright (c) 2022, Leam Technology Systems and contributors
# For license information, please see license.txt

from renovation.model import map_doctype
from pms_app.pms_core.models.pms_contact.pms_contact import PMSContact as _PMSContact

map_doctype("PMS Contact", _PMSContact)


class PMSContact(_PMSContact):
    pass
