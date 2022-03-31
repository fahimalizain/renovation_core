# Copyright (c) 2022, Leam Technology Systems and contributors
# For license information, please see license.txt

# import frappe
from renovation.model import map_doctype
from pms_manager.pms_customer.models.pms_customer.pms_customer import PMSCustomer as _PMSCustomer

map_doctype("PMS Customer", _PMSCustomer)


class PMSCustomer(_PMSCustomer):
    pass
