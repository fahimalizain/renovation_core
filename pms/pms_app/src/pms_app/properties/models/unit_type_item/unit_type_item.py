
import renovation
from renovation import RenovationModel
from .unit_type_item_types import UnitTypeItemMeta
from pms_app.properties.exceptions import UnitTypeNotFound


class UnitTypeItem(RenovationModel["UnitTypeItem"], UnitTypeItemMeta):
    async def validate_unit_type_enabled(self):
        from pms_app.properties.models.unit_type.unit_type import UnitType
        if not await UnitType.get_value(self.unit_type, "enabled"):
            raise UnitTypeNotFound(renovation._(
                "Disabled Unit Type found in Unit Types No. {0}: '{1}'"
            ).format(self.idx, self.unit_type))
