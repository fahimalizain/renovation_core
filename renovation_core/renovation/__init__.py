
__version__ = '0.0.1'

from .orm import Field, Column  # noqa
from .model import FrappeModel as RenovationModel  # noqa

# Useful utilities
from frappe import (local, _, parse_json, _dict, get_module, get_hooks, get_traceback, scrub)  # noqa


def get_attr(method_string):
    """Get python method object from its name."""
    # app_name = method_string.split(".")[0]
    # if not local.flags.in_uninstall and not local.flags.in_install and app_name not in get_installed_apps():
    # 	throw(_("App {0} is not installed").format(app_name), AppNotInstalledError)

    modulename = '.'.join(method_string.split('.')[:-1])
    methodname = method_string.split('.')[-1]
    return getattr(get_module(modulename), methodname)
