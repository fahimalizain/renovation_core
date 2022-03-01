from todo_app.models.order_workflow import OrderWorkflow


async def create_order(order):
    order_doc = OrderWorkflow()
    order_doc.update(order)
    order_doc = await order_doc.save()
    return {
        "name": order_doc.name,
        "status": order_doc.order_workflow_state,
        "order_name": order_doc.order_name,
        "grand_total": order_doc.grand_total,
    }
