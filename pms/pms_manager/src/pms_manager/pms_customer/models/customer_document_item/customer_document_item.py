
from renovation import RenovationModel
from .customer_document_item_types import CustomerDocumentItemMeta


class CustomerDocumentItem(RenovationModel["CustomerDocumentItem"], CustomerDocumentItemMeta):
    pass
