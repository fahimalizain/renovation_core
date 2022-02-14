from asyncer import asyncify as _asyncify

import frappe
import sys
import anyio
from typing import Callable, Optional, Awaitable, TypeVar
if sys.version_info >= (3, 10):
    from typing import ParamSpec
else:
    from typing_extensions import ParamSpec

from frappe.database import get_db


def thread_safe_db(db):
    import threading

    def lock_fn(fn):
        lock = threading.RLock()

        def inner(*args, **kwargs):
            with lock:
                return fn(*args, **kwargs)

        return inner

    db.sql = lock_fn(db.sql)


T_Retval = TypeVar("T_Retval")
T_ParamSpec = ParamSpec("T_ParamSpec")
T = TypeVar("T")


def asyncify(
    function: Callable[T_ParamSpec, T_Retval],
    *,
    cancellable: bool = False,
    limiter: Optional[anyio.CapacityLimiter] = None
) -> Callable[T_ParamSpec, Awaitable[T_Retval]]:

    def wrap_db(fn):
        def inner(*args, **kwargs):
            frappe.local.db = get_db(user=frappe.local.conf.db_name)
            try:
                val = fn(*args, **kwargs)
            finally:
                frappe.local.db.close()

            return val

        return inner

    return _asyncify(function=wrap_db(function), cancellable=cancellable, limiter=limiter)
