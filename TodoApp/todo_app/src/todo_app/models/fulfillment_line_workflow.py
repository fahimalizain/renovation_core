from renovation import RenovationModel
from todo_app.fsm_workflows.order_workflow.order_workflow_frappe import \
    FulfillmentLineWorkflowMachineMixin


class FulfillmentLinkWorkflow(RenovationModel["FulfillmentLinkWorkflow"],
                              FulfillmentLineWorkflowMachineMixin):
    wf_state = "status"
    wf_date = "workflow_date"

    async def item_out_for_delivery(self):
        await self._item_out_for_delivery()
        return self

    async def item_delivered(self):
        await self._item_delivered()
        return self
