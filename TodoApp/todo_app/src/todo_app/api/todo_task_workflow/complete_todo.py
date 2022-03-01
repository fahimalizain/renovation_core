from todo_app.api import router
import todo_app.controllers.todo as todo_controllers


@router.put("/complete-todo/{todo_name}")
async def complete_todo(todo_name: str):
    return await todo_controllers.complete_todo(todo_name)
