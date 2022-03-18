from todo_app.api import router
import todo_app.controllers.order as order_controllers


@router.put("/cancel-order/{order_name}")
async def cancel_order(order_name):
    return await order_controllers.cancel_order(order_name)
