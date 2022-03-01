from renovation import RenovationModel
from todo_app.fsm_workflows.order_workflow.order_workflow_frappe import OrderWorkflowMachineMixin


class OrderWorkflow(RenovationModel["OrderWorkflow"], OrderWorkflowMachineMixin):
    wf_state = "order_workflow_state"
    wf_date = "order_workflow_date"

    async def make_order_payment(self, paid_amount):
        from todo_app.models.payment_workflow import PaymentWorkflow
        payment_doc = await PaymentWorkflow.exists({"order": self.name})

        if not payment_doc:
            payment = PaymentWorkflow()
            payment.order = self.name
            payment_doc = await payment.save()
        else:
            payment_doc = await PaymentWorkflow.get_doc(payment_doc)
        payment_doc.paid_amount = paid_amount
        await payment_doc.mark_as_paid()
        await payment_doc.save()
        return payment_doc

    async def confirm_order(self):
        return await self._confirm_order()

    async def cancel_order(self):
        return await self._cancel_order()

    async def fulfiill_order(self):
        return await self._fulfill_order()

    async def submit_order(self):
        return await self._submit_order()
