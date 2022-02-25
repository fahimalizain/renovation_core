from typing import Optional
from pms_app.properties.models.unit_type import UnitType


async def create_unit_type(
        title: str, enabled: bool = True, unit_attributes: Optional[list] = None):

    if not unit_attributes:
        unit_attributes = []

    _unit_attributes = []
    for unit_attribute in unit_attributes:
        unit_attribute["attribute_type"] = \
            unit_attribute["attribute_type"].title().replace("_", "-")
        _unit_attributes.append(unit_attribute)

    doc = UnitType(dict(
        title=title,
        enabled=enabled,
        unit_attributes=_unit_attributes
    ))
    await doc.insert()

    return doc
