
from renovation import RenovationModel
from .pms_custom_field_value_types import PMSCustomFieldValueMeta


class PMSCustomFieldValue(RenovationModel["PMSCustomFieldValue"], PMSCustomFieldValueMeta):
    pass
