from typing import List, Optional
from pms_app.properties.models.unit_attribute_item.unit_attribute_item import UnitAttributeItem


class UnitMeta:
    active: Optional[int]
    unit_name: str
    unit_number: Optional[int]
    description: Optional[str]
    unit_type: str
    size: Optional[float]
    unit_attributes: List[UnitAttributeItem]
