from renovation import _
from pms_app.properties.exceptions import UnitNotFound
from pms_app.properties.models.unit import Unit


async def delete_unit(name: str):
    if not await Unit.exists(name):
        raise UnitNotFound(message=(_("Unit with name '{0}' not found.")).format(name))

    doc = await Unit.get_doc(name)
    await doc.delete()

    return doc
