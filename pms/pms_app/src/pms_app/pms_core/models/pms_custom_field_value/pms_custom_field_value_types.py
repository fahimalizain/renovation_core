from typing import Optional


class PMSCustomFieldValueMeta:
    fieldname: str
    entity_type: str
    entity: str
    value: Optional[str]
