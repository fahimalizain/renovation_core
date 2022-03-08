
from renovation import _
from pms_app.properties.exceptions import PropertyNotFound
from pms_app.properties.models import Property


async def delete_property(name: str):
    if not await Property.exists(name):
        raise PropertyNotFound(message=(
            _("Property with name '{0}' not found.")
        ).format(name))

    doc = await Property.get_doc(name)
    await doc.delete()

    return True
