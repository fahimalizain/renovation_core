# Copyright (c) 2022, Leam Technology Systems and contributors
# For license information, please see license.txt

# import frappe
from renovation.model import map_doctype
from pms_manager.pms_customer.models.customer_document_type.customer_document_type import \
    CustomerDocumentType as _CustomerDocumentType

map_doctype("Customer Document Type", _CustomerDocumentType)


class CustomerDocumentType(_CustomerDocumentType):
    pass
