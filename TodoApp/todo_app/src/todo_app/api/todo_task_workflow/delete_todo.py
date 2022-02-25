from todo_app.api import router
import todo_app.controllers as todo_controllers


@router.delete("/delete-todo/{todo_name}")
async def delete_todo(todo_name: str):
    return await todo_controllers.delete_todo(todo_name)
