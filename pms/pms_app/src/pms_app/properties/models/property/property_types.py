from typing import Optional


class PropertyMeta:
    active: Optional[int]
    property_name: str
    property_type: str
    description: Optional[str]
    address: Optional[str]
    city: Optional[str]
    beneficiary: str
    # units: List[UnitItem]
