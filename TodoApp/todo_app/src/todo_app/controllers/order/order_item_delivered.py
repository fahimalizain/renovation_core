from todo_app.models.fulfillment_workflow import FulfillmentWorkflow


async def item_delivered(fulfillment_name, fulfillment_line):
    fulfillment_doc = await FulfillmentWorkflow.get_doc(fulfillment_name)
    resp = await fulfillment_doc.fulfillment_line_delivered(fulfillment_line)
    order_doc = resp.get("order_doc")
    fulfillment_doc = resp.get("fulfillment_doc")
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
