import renovation
from pms_app.utils import PMSException


class UnitAttributeError(PMSException):
    def __init__(self, message: str = None, data=None) -> None:
        self.http_status_code = 400
        self.error_code = "UNIT_ATTRIBUTES_ERROR"

        self.message = message or renovation._("Error in Unit Attributes")
        self.data = data or renovation._dict()


class UnitTypeNotFound(PMSException):
    def __init__(self, message: str = None, data=None) -> None:
        self.http_status_code = 404
        self.error_code = "UNIT_TYPE_NOT_FOUND"

        self.message = message or renovation._("Unit Type not found.")
        self.data = data or renovation._dict()


class UnitNotFound(PMSException):
    def __init__(self, message: str = None, data=None) -> None:
        self.http_status_code = 404
        self.error_code = "UNIT_NOT_FOUND"

        self.message = message or renovation._("Unit not found.")
        self.data = data or renovation._dict()


class UnitError(PMSException):
    def __init__(self, message: str = None, data=None) -> None:
        self.http_status_code = 400
        self.error_code = "UNIT_ERROR"

        self.message = message or renovation._("Error in Unit.")
        self.data = data or renovation._dict()


class UnitItemError(PMSException):
    def __init__(self, message: str = None, data=None) -> None:
        self.http_status_code = 400
        self.error_code = "UNIT_ITEM_ERROR"

        self.message = message or renovation._("Error in Unit Items.")
        self.data = data or renovation._dict()


class PropertyTypeNotEnabled(PMSException):
    def __init__(self, message: str = None, data=None) -> None:
        self.http_status_code = 400
        self.error_code = "UNIT_TYPE_ERROR"

        self.message = message or renovation._("Unit Type not enabled.")
        self.data = data or renovation._dict()


class PropertyTypeNotFound(PMSException):
    def __init__(self, message: str = None, data=None) -> None:
        self.http_status_code = 404
        self.error_code = "PROPERTY_TYPE_NOT_FOUND"

        self.message = message or renovation._("Property Type not found.")
        self.data = data or renovation._dict()


class PropertyNotFound(PMSException):
    def __init__(self, message: str = None, data=None) -> None:
        self.http_status_code = 404
        self.error_code = "PROPERTY_NOT_FOUND"

        self.message = message or renovation._("Property not found.")
        self.data = data or renovation._dict()
