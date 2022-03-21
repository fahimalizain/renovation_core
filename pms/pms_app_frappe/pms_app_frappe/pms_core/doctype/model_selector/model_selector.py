# Copyright (c) 2022, Leam Technology Systems and contributors
# For license information, please see license.txt

# import frappe
from renovation.model import map_doctype
from pms_app.pms_core.models.model_selector.model_selector import ModelSelector as _ModelSelector

map_doctype("Model Selector", _ModelSelector)


class ModelSelector(_ModelSelector):
    pass
