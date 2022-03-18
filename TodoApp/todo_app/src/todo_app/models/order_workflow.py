import frappe
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
        await payment_doc.add_payment()
        await payment_doc.save()
        return payment_doc

    async def confirm_order(self):
        return await self._confirm_order()

    async def cancel_order(self):
        return await self._cancel_order()

    async def fulfiill_order(self, items):
        return await self._fulfill_order(items)

    async def submit_order(self):
        return await self._submit_order()

    async def order_fulfilled(self):
        await self._order_fulfilled()
        return self

    async def create_fulfillment_lines(self, event):
        from todo_app.models.fulfillment_workflow import FulfillmentWorkflow
        items = event.args[0].get("items")
        doc = FulfillmentWorkflow()
        doc.order = self.name
        fulfillment_lines = [
            {"order_workflow_item": item.get("name")} for item in items
        ]
        doc.extend("fulfillment_line_workflows", fulfillment_lines)
        await doc.save()
        return doc

    async def after_order_fulfill(self, *args):
        # lets reset the status that was set
        import asyncer
        await asyncer.asyncify(self.load_doc_before_save)()
        if self.has_value_changed(self.wf_state) and self.get_doc_before_save():
            previous = self.get_doc_before_save()
            self.set(self.wf_state, previous.get(self.wf_state))

    async def is_all_items_fulfilled(self, *args, **kwargs):
        from todo_app.models.fulfillment_workflow import FulfillmentWorkflow
        from todo_app.fsm_workflows.order_workflow.order_workflow_status_base import \
            FulfillmentLineWorkflowStatus
        fulfillment = await FulfillmentWorkflow.exists({"order": self.name})
        fulfillment_doc = await FulfillmentWorkflow.get_doc(fulfillment)
        return all(
            fulfillment.status == FulfillmentLineWorkflowStatus.DELIVERED
            for fulfillment in fulfillment_doc.fulfillment_line_workflows
        )

    async def is_all_items_not_fulfilled(self, *args, **kwargs):
        from todo_app.models.fulfillment_workflow import FulfillmentWorkflow
        from todo_app.fsm_workflows.order_workflow.order_workflow_status_base import \
            FulfillmentLineWorkflowStatus
        fulfillment = await FulfillmentWorkflow.exists({"order": self.name})
        fulfillment_doc = await FulfillmentWorkflow.get_doc(fulfillment)
        return any(
            fulfillment.status != FulfillmentLineWorkflowStatus.DELIVERED
            for fulfillment in fulfillment_doc.fulfillment_line_workflows
        )
