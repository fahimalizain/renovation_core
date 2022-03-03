from typing import Optional, List
from pms_app.properties.models.unit_item.unit_item import UnitItem


class PropertyMeta:
    active: Optional[int]
    property_name: str
    property_type: str
    description: Optional[str]
    address: Optional[str]
    city: Optional[str]
    beneficiary: str
    units: List[UnitItem]
