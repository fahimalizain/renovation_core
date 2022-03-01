from todo_app.models.order_workflow import OrderWorkflow


async def make_order_payment(order_name, paid_amount):
    order_doc = await OrderWorkflow.get_doc(order_name)
    payment_doc = await order_doc.make_order_payment(paid_amount)
    order_doc = await OrderWorkflow.get_doc(order_name)
    return {
        "name": order_doc.name,
        "order_status": order_doc.order_workflow_state,
        "order_name": order_doc.order_name,
        "grand_total": order_doc.grand_total,
        "payment_status": payment_doc.payment_workflow,
        "paid_amount": payment_doc.paid_amount
    }
