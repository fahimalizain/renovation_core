# Copyright (c) 2022, LEAM and contributors
# For license information, please see license.txt

from todo_app.models.order_workflow import OrderWorkflow as _OrderWorkflow
from renovation.model import map_doctype

map_doctype("Order Workflow", _OrderWorkflow)


class OrderWorkflow(_OrderWorkflow):
    pass
