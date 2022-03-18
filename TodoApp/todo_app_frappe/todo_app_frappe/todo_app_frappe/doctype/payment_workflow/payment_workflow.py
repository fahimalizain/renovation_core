# Copyright (c) 2022, LEAM and contributors
# For license information, please see license.txt

from todo_app.models.payment_workflow import PaymentWorkflow as _PaymentWorkflow
from renovation.model import map_doctype

map_doctype("Payment Workflow", _PaymentWorkflow)


class PaymentWorkflow(_PaymentWorkflow):
    pass
