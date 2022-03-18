# -*- coding: utf-8 -*-
# Copyright (c) 2021, LEAM Technology System. and contributors
# For license information, please see license.txt


def check_if_valid_transition(status: str, field_name: str):
    def inner(func):
        import functools
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            _current_status = args[0].get(field_name)
            doctype = args[0].get("doctype")
            docname = args[0].get("name")
            if _current_status != status:
                from transitions import MachineError
                msg = "Can't edit doctype %s %s in state %s!" % (
                    doctype, docname, _current_status)
                raise MachineError(msg)
            value = func(*args, **kwargs)

            return value

        return wrapper

    return inner
