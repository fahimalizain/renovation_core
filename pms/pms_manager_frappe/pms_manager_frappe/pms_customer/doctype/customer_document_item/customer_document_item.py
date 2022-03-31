# Copyright (c) 2022, Leam Technology Systems and contributors
# For license information, please see license.txt

# import frappe
from renovation.model import map_doctype
from pms_manager.pms_customer.models.customer_document_item.customer_document_item import \
    CustomerDocumentItem as _CustomerDocumentItem

map_doctype("Customer Document Item", _CustomerDocumentItem)


class CustomerDocumentItem(_CustomerDocumentItem):
    pass
