from todo_app.api import router
import todo_app.controllers as todo_controllers


@router.post("/create-todo/")
async def create_todo(todo: dict):
    return await todo_controllers.create_todo(todo)
