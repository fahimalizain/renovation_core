
from renovation import RenovationModel
from .unit_item_types import UnitItemMeta


class UnitItem(RenovationModel["UnitItem"], UnitItemMeta):
    pass
