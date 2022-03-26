import renovation

from pms_app.utils.exceptions import PermissionDenied
from pms_app.pms_core.models.pms_custom_field.pms_custom_field import \
    PMS_CUSTOMIZABLE_ENTITY_TYPES_HOOK


async def get_customizable_entity_types():
    if "Sys Admin" not in renovation.get_roles():
        raise PermissionDenied(message=renovation._(
            "Only users with role 'Sys Admin' can perform this action"))

    entity_types = set(renovation.get_hooks(PMS_CUSTOMIZABLE_ENTITY_TYPES_HOOK))
    return list(entity_types)
