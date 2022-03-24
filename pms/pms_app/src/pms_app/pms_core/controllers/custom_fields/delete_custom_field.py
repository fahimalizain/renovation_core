import renovation

from pms_app.pms_core.models.pms_custom_field.pms_custom_field import PMSCustomField
from pms_app.utils.exceptions import PermissionDenied, NotFound


async def delete_custom_field(custom_field: str):
    if "Sys Admin" not in renovation.get_roles():
        raise PermissionDenied(message=renovation._(
            "Only users with role 'Sys Admin' can perform this action"))

    if not await PMSCustomField.exists(custom_field):
        raise NotFound(
            message=renovation._("Custom Field: {0} not found").format(custom_field),
            custom_field=custom_field
        )

    r = await PMSCustomField.get_doc(custom_field)
    await r.delete()

    return True
