
__version__ = '0.0.1'

from .orm import Field, Column  # noqa
from .model import FrappeModel as RenovationModel  # noqa


class _dict(dict):
    """dict like object that exposes keys as attributes"""

    def __getattr__(self, key):
        ret = self.get(key)
        # "__deepcopy__" exception added to fix frappe#14833 via DFP
        if not ret and key.startswith("__") and key != "__deepcopy__":
            raise AttributeError()
        return ret

    def __setattr__(self, key, value):
        self[key] = value

    def __getstate__(self):
        return self

    def __setstate__(self, d):
        self.update(d)

    def update(self, d):
        """update and return self -- the missing dict feature in python"""
        super(_dict, self).update(d)
        return self

    def copy(self):
        return _dict(dict(self).copy())
