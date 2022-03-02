
from renovation import _
from pms_app.properties.exceptions import PropertyTypeNotFound
from pms_app.properties.models.property_type.property_type import PropertyType


async def delete_property_type(name: str):
    if not await PropertyType.exists(name):
        raise PropertyTypeNotFound(message=(
            _("Property Type with name '{0}' not found.")
        ).format(name))

    doc = await PropertyType.get_doc(name)
    await doc.delete()

    return True
