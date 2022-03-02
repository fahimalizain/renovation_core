
from renovation import _
from pms_app.properties.exceptions import PropertyTypeNotFound
from pms_app.properties.models.property_type.property_type import PropertyType


async def update_property_type(name: str, input):

    if not await PropertyType.exists(name):
        raise PropertyTypeNotFound(
            message=(_(
                "Property Type with name '{0}' not found."
            )).format(name)
        )

    doc = await PropertyType.get_doc(name)

    # If any unit types were passed in, handle them
    if input.get("unit_types"):
        unit_types = input.get("unit_types")
        doc.unit_types = []
        del input["unit_types"]

        for unit_type in unit_types:
            doc.append("unit_types", unit_type)

    doc.update(input)
    await doc.save()

    return doc
