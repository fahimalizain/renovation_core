from renovation import _
from pms_app.properties.models import UnitType
from pms_app.properties.exceptions import UnitTypeNotFound


async def delete_unit_type(name: str):

    if not await UnitType.exists(name):
        raise UnitTypeNotFound(message=(_("Unit Type with name '{0}' not found.")).format(name))

    doc = await UnitType.get_doc(name)
    await doc.delete()

    return True
