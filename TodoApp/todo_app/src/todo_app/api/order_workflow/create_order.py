from todo_app.api import router
import todo_app.controllers.order as order_controllers


@router.post("/create-order/")
async def create_order(order: dict):
    return await order_controllers.create_order(order)
