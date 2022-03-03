# Copyright (c) 2022, LEAM and contributors
# For license information, please see license.txt

from todo_app.models.fulfillment_line_workflow import \
    FulfillmentLinkWorkflow as _FulfillmentLinkWorkflow
from renovation.model import map_doctype

map_doctype("Fulfillment Line Workflow", _FulfillmentLinkWorkflow)


class FulfillmentLineWorkflow(_FulfillmentLinkWorkflow):
    pass
