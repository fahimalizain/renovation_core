# Copyright (c) 2022, LEAM and contributors
# For license information, please see license.txt

from todo_app.models.fulfillment_workflow import FulfillmentWorkflow as _FulfillmentWorkflow
from renovation.model import map_doctype

map_doctype("Fulfillment Workflow", _FulfillmentWorkflow)


class FulfillmentWorkflow(_FulfillmentWorkflow):
    pass
