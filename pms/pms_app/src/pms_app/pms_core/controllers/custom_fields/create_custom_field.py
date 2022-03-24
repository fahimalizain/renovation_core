import renovation
from pms_app.utils.exceptions import PermissionDenied
from pms_app.pms_core.models.pms_custom_field.pms_custom_field import PMSCustomField


async def create_custom_field(data: dict):
    if "Sys Admin" not in renovation.get_roles():
        raise PermissionDenied(message=renovation._(
            "Only users with role 'Sys Admin' can perform this action"))

    r = PMSCustomField(data)
    await r.insert()

    return r
