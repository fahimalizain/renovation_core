from todo_app.api import router
import todo_app.controllers.todo as todo_controllers


@router.get("/get-todo/{todo_name}")
async def get_todo(todo_name):
    return await todo_controllers.get_todo(todo_name)
