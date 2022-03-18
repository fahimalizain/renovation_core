from todo_app.api import router
import todo_app.controllers.order as order_controllers


@router.put("/fulfill-order/{order_name}")
async def fulfill_order(order_name: str, items: dict):
    return await order_controllers.fulfill_order(order_name, items)
