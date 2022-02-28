
from typing import Optional
import renovation

from pms_app.properties.models.property import Property


async def create_property(
    property_name: str,
    property_type: str,
    beneficiary: str,
    active: int = 1,
    description: str = None,
    address: str = None,
    city: str = None,
    units: Optional[list] = None
):

    if not units:
        units = []

    doc = Property(renovation._dict(
        doctype="Property",
        property_name=property_name,
        property_type=property_type,
        beneficiary=beneficiary,
        active=active,
        description=description,
        address=address,
        city=city,
        units=units
    ))
    await doc.insert()

    return doc
