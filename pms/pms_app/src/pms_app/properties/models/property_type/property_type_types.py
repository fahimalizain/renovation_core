from typing import List, Optional
from pms_app.properties.models.unit_type_item.unit_type_item import UnitTypeItem


class PropertyTypeMeta:
    enabled: Optional[int]
    title: str
    has_units: Optional[int]
    unit_types: List[UnitTypeItem]
