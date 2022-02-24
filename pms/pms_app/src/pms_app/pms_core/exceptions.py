import renovation
from pms_app.utils import PMSException


class PMSContactNotFound(PMSException):
    def __init__(self, pms_contact: str):
        self.http_status_code = 404
        self.error_code = "PMS_CONTACT_NOT_FOUND"
        self.message = renovation._("PMS Contact not found")
        self.data = renovation._dict(
            pms_contact=pms_contact
        )


class MissingContactInfo(PMSException):
    def __init__(self, message: str = None, data=None):
        self.http_status_code = 400
        self.error_code = "MISSING_CONTACT_INFO"
        self.message = message or renovation._(
            "Please fill out required information to make the update")
        self.data = data or renovation._dict()
