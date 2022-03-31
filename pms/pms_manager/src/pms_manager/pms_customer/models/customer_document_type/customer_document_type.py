
from renovation import RenovationModel
from .customer_document_type_types import CustomerDocumentTypeMeta


class CustomerDocumentType(RenovationModel["CustomerDocumentType"], CustomerDocumentTypeMeta):
    pass
