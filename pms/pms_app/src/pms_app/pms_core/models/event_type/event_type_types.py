from typing import List, Optional
from pms_app.pms_core.models.model_selector.model_selector import ModelSelector


class EventTypeMeta:
    title: str
    roles: List[dict]
    models: List[ModelSelector]
    actions: Optional[str]
    action_info: Optional[str]
