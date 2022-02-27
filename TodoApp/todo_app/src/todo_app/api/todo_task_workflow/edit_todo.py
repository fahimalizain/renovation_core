from todo_app.api import router
import todo_app.controllers as todo_controllers


@router.put("/edit-todo/{todo_name}")
async def edit_todo(todo_name: str, task_description=None, task_name=None):
    return await todo_controllers.edit_todo(todo_name, task_name, task_description)
