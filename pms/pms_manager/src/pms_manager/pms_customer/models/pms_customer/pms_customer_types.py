from typing import List, Optional
from pms_manager.pms_customer.models.customer_document_item.customer_document_item import \
    CustomerDocumentItem


class PMSCustomerMeta:
    slug: str
    user: Optional[str]
    company_email: Optional[str]
    company_representative: str
    company_representative_name: Optional[str]
    company_name: Optional[str]
    company_address: Optional[str]
    notify_email: Optional[int]
    notify_sms: Optional[int]
    notify_telegram: Optional[int]
    notify_whatsapp: Optional[int]
    documents: List[CustomerDocumentItem]
    company_email_verified: Optional[int]
