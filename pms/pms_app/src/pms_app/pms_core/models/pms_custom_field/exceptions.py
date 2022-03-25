import renovation
from pms_app.utils import PMSException


class InvalidCustomFieldOption(PMSException):
    def __init__(self, fieldname, fieldtype, options, message=None) -> None:
        self.error_code = "INVALID_CUSTOM_FIELD_OPTION"
        self.message = message or renovation._("Invalid Custom Field Option")
        self.http_status_code = 400
        self.data = renovation._dict(
            fieldname=fieldname, fieldtype=fieldtype, options=options
        )
