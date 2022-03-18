from todo_app.models.fulfillment_workflow import FulfillmentWorkflow
from todo_app.models.order_workflow import OrderWorkflow


async def fulfill_order(order_name, items):
    order_doc = await OrderWorkflow.get_doc(order_name)
    await order_doc.fulfiill_order(items)
    fulfillment = await FulfillmentWorkflow.exists({"order": order_doc.name})
    fulfillment_doc = await FulfillmentWorkflow.get_doc(fulfillment)
    return {
        "name": order_doc.name,
        "status": order_doc.order_workflow_state,
        "order_name": order_doc.order_name,
        "order_items": [{"name": order_item.get("name"), "item": order_item.get("item")} for
                        order_item in order_doc.get("order_workflow_items")],

        "grand_total": order_doc.grand_total,
        "fulfillment": fulfillment_doc.name,
        "fulfillment_lines": [
            {"name": line.get("name"), "order_workflow_item": line.get("order_workflow_item"),
             "status": line.get("status")} for line in
            fulfillment_doc.get("fulfillment_line_workflows")]
    }
