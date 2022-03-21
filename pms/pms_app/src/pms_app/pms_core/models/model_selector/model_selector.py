
from renovation import RenovationModel
from .model_selector_types import ModelSelectorMeta


class ModelSelector(RenovationModel["ModelSelector"], ModelSelectorMeta):
    pass
