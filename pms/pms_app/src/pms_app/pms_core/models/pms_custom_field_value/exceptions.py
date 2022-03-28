from typing import List

import renovation
from pms_app.utils import PMSException


class InvalidValueForSelectField(PMSException):
    def __init__(self, fieldname, options, value):
        self.error_code = "INVALID_VALUE_FOR_SELECT_FIELD"
        self.http_status_code = 400
        self.message = renovation._("Invalid value for Select field")
        self.data = renovation._dict(
            fieldname=fieldname,
            options=options,
            value=value
        )


class CustomFieldNotApplicableOnEntityType(PMSException):
    def __init__(
            self,
            cf_label: str,
            cf_fieldname,
            valid_entity_types: List[str],
            current_type: str):
        self.error_code = "CF_NOT_APPLICABLE_ON_ENTITY_TYPE"
        self.http_status_code = 400
        self.message = renovation._(
            "Custom Field not applicable on Entity Type: {0}").format(current_type)
        self.data = renovation._dict(
            cf_fieldname=cf_fieldname,
            cf_label=cf_label, valid_entity_types=valid_entity_types, current_type=current_type
        )
