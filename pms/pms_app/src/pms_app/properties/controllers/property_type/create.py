
from typing import Optional
from pms_app.properties.models.property_type.property_type import PropertyType


async def create_property_type(
        title: str,
        enabled: int = 1,
        has_units: int = 0,
        unit_types: Optional[list] = None
):

    if not unit_types:
        unit_types = []

    doc = PropertyType(dict(
        title=title,
        enabled=enabled,
        has_units=has_units,
        unit_types=unit_types
    ))
    await doc.insert()

    return doc
