
from renovation import RenovationModel
from .unit_type_item_types import UnitTypeItemMeta


class UnitTypeItem(RenovationModel["UnitTypeItem"], UnitTypeItemMeta):
    pass
