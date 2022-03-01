import frappe
from renovation import RenovationModel
from todo_app.fsm_workflows.order_workflow.order_workflow_frappe import PaymentWorkflowMachineMixin
from todo_app.fsm_workflows.order_workflow.order_workflow_status_base import PaymentWorkflowStatus


class PaymentWorkflow(RenovationModel["PaymentWorkflow"], PaymentWorkflowMachineMixin):
    wf_state = "payment_workflow"
    wf_date = "payment_workflow_date"

    async def mark_as_paid(self):
        return await self._mark_as_paid()

    async def is_fully_charged(self, *args, **kwargs):
        from todo_app.models.order_workflow import OrderWorkflow
        doc = await OrderWorkflow.get_doc(self.get("order"))
        order_grand_total = doc.grand_total
        return self.get("paid_amount") >= order_grand_total

    async def submit_order(self, *args, **kwargs):
        from todo_app.models.order_workflow import OrderWorkflow
        doc = await OrderWorkflow.get_doc(self.get("order"))
        doc.machine.set_state(f"{PaymentWorkflowStatus.NAME}_{PaymentWorkflowStatus.FULLY_CHARGED}")
        await doc.submit_order()
        await doc.save()
