from todo_app.api import router
import todo_app.controllers.todo as todo_controllers


@router.get("/get-todos")
async def get_todos():
    return await todo_controllers.get_todos()
