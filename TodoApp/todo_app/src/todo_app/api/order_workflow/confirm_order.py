from todo_app.api import router
import todo_app.controllers.order as order_controllers


@router.put("/confirm-order/{order_name}")
async def confirm_order(order_name):
    return await order_controllers.confirm_order(order_name)
