from todo_app.api import router
import todo_app.controllers.order as order_controllers


@router.put("/item-delivered/{fulfillment_name}/{fulfillment_line}")
async def item_delivered(fulfillment_name, fulfillment_line):
    return await order_controllers.item_delivered(fulfillment_name, fulfillment_line)
