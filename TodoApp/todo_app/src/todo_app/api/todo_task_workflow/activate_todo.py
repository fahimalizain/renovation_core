from todo_app.api import router
import todo_app.controllers as todo_controllers


@router.put("/activate-todo/{todo_name}")
async def activate_todo(todo_name):
    return await todo_controllers.activate_todo(todo_name)
