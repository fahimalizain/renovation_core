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


class NonCustomizableEntityType(PMSException):
    def __init__(self, entity_type: str):
        self.error_code = "ENTITY_TYPE_IS_NOT_CUSTOMIZABLE"
        self.http_status_code = 400
        self.message = renovation._("EntityType: {0} is not customizable").format(entity_type)
        self.data = renovation._dict(
            entity_type=entity_type
        )


class DuplicateFieldname(PMSException):
    def __init__(self, fieldname, fieldtype, options, entity_type: str):
        self.error_code = "DUPLICATE_FIELDNAME"
        self.http_status_code = 400
        self.message = renovation._(
            "EntityType: {0} has another field with name: {1}").format(entity_type, fieldname)
        self.data = renovation._dict(
            fieldname=fieldname, fieldtype=fieldtype, options=options,
            entity_type=entity_type
        )
