from todo_app.api import router
import todo_app.controllers as todo_controllers


@router.put("/revert-deleted-todo/{todo_name}")
async def revert_delete_todo(todo_name):
    return await todo_controllers.revert_delete_todo(todo_name)
