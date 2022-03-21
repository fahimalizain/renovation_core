from typing import Optional, List
from pms_app.pms_core.models.model_selector.model_selector import ModelSelector


class EventTypeMeta:
    title: str
    actions: Optional[str]
    roles: List[dict]
    models: List[ModelSelector]
