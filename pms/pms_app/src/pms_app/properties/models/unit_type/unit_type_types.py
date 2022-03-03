from typing import List, Optional
from pms_app.properties.models.unit_type_attribute_item.unit_type_attribute_item import UnitTypeAttributeItem


class UnitTypeMeta:
    enabled: Optional[int]
    title: str
    unit_attributes: List[UnitTypeAttributeItem]
