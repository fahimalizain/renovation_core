from typing import Optional, List
from pms_app.pms_core.models.model_selector.model_selector import ModelSelector


class PMSCustomFieldMeta:
    enabled: Optional[int]
    label: str
    fieldname: Optional[str]
    fieldtype: str
    options: Optional[str]
    description: Optional[str]
    insert_after: Optional[str]
    entity_type: Optional[str]
    entity: Optional[str]
    entities_excluded: List[ModelSelector]
