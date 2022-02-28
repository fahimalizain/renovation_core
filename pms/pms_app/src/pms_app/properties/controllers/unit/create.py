from typing import Optional
from pms_app.properties.models.unit import Unit


async def create_unit(
    unit_name: str,
    unit_type: str,
    unit_number: int = None,
    description: str = None,
    active: int = 1,
    size: float = None,
    unit_attributes: Optional[list] = None
):

    if not unit_attributes:
        unit_attributes = []

    doc = Unit(dict(
        unit_name=unit_name,
        unit_type=unit_type,
        unit_number=unit_number,
        description=description,
        active=active,
        size=size,
        unit_attributes=unit_attributes
    ))
    await Unit.insert()

    return doc
