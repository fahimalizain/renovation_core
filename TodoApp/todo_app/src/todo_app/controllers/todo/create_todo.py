from todo_app.models.todo_workflow import TodoTaskWorkflow


async def create_todo(todo: dict):
    todo_doc = TodoTaskWorkflow()
    todo_doc.update(todo)
    created_todo = await todo_doc.save()
    return {
        "name": created_todo.name,
        "task_name": created_todo.task_name,
        "status": created_todo.workflow_state,
        "task_description": created_todo.task_description
    }
