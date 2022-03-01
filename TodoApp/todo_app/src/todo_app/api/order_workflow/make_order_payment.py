from todo_app.api import router
import todo_app.controllers.order as order_controllers


@router.post("/make-order-payment/{order_name}")
async def make_order_payment(order_name: str, update: dict):
    return await order_controllers.make_order_payment(order_name, update.get("paid_amount"))
