from typing import Optional


class PMSContactMeta:
    enabled: Optional[int]
    user: Optional[str]
    first_name: str
    last_name: Optional[str]
    email_id: Optional[str]
    mobile_no: Optional[str]
    contact_type: Optional[str]
    address: Optional[str]
    national_id: Optional[str]
    national_id_expiry: Optional[str]
    is_company: Optional[int]
    company_name: Optional[str]
    company_representative_contact: Optional[str]
    company_representative_name: Optional[str]
    notify_email: Optional[int]
    notify_sms: Optional[int]
    notify_telegram: Optional[int]
    notify_whatsapp: Optional[int]
