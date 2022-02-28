
from renovation import _
from pms_app.properties.exceptions import PropertyNotFound
from pms_app.properties.models.property import Property


async def update_property(name: str, input):
    if not await Property.exists(name):
        raise PropertyNotFound(
            message=(_(
                "Property with name '{0}' not found."
            )).format(name)
        )

    doc = await Property.get_doc(name)

    if input.get("units"):
        doc.units = []
        units = input.get("units")
        del input["units"]

        # If name of the Unit Item was passed in, update it, otherwise make new one
        for unit in units:
            doc.append("units", unit)

    doc.update(input)
    await doc.save()

    return doc
