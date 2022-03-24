from typing import List, Optional
from pms_app.pms_core.models.model_selector.model_selector import ModelSelector


class PMSCustomFieldMeta:
    enabled: Optional[int]
    title: str
    fieldname: Optional[str]
    description: Optional[str]
    fieldtype: str
    options: Optional[str]
    insert_after: Optional[str]
    entity_type: Optional[str]
    entity: Optional[str]
    entities_excluded: List[ModelSelector]
