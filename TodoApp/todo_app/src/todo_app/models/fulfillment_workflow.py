import frappe
from renovation import RenovationModel


class FulfillmentWorkflow(RenovationModel["FulfillmentWorkflow"]):
    async def fulfillment_line_out_for_delivery(self, line):
        from todo_app.models.fulfillment_line_workflow import FulfillmentLinkWorkflow
        fulfillment_line_doc = await FulfillmentLinkWorkflow.get_doc(line)
        fulfillment_line_doc = await fulfillment_line_doc.item_out_for_delivery()
        self.fulfillment_line_workflows = [fulfillment_line_workflow for fulfillment_line_workflow
                                           in self.fulfillment_line_workflows if
                                           fulfillment_line_workflow.name != line]
        self.append("fulfillment_line_workflows", fulfillment_line_doc)
        await self.save()
        from todo_app.models.order_workflow import OrderWorkflow
        order_doc = await OrderWorkflow.get_doc(self.get("order"))
        return {"fulfillment_doc": self, "order_doc": order_doc}

    async def fulfillment_line_delivered(self, line):
        from todo_app.models.fulfillment_line_workflow import FulfillmentLinkWorkflow
        fulfillment_line_doc = await FulfillmentLinkWorkflow.get_doc(line)
        fulfillment_line_doc = await fulfillment_line_doc.item_delivered()
        self.fulfillment_line_workflows = [fulfillment_line_workflow for fulfillment_line_workflow
                                           in self.fulfillment_line_workflows if
                                           fulfillment_line_workflow.name != line]
        self.append("fulfillment_line_workflows", fulfillment_line_doc)
        await self.save()
        from todo_app.models.order_workflow import OrderWorkflow
        order_doc = await OrderWorkflow.get_doc(self.get("order"))
        from todo_app.fsm_workflows.order_workflow.order_workflow_status_base import \
            FulfillmentLineWorkflowStatus
        order_doc.machine.set_state(
            f"{FulfillmentLineWorkflowStatus.NAME}_{FulfillmentLineWorkflowStatus.DELIVERED}")
        order_doc = await order_doc.order_fulfilled()
        order_doc = await order_doc.save()
        return {"fulfillment_doc": self, "order_doc": order_doc}
