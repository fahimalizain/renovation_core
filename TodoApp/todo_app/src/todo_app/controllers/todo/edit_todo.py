from todo_app.models.todo_workflow import TodoTaskWorkflow


async def edit_todo(todo_name, task_name, task_description):
    todo_doc = await TodoTaskWorkflow.get_doc(todo_name)
    await todo_doc.edit_todo(task_name, task_description)
    return {
        "name": todo_doc.name,
        "task_name": todo_doc.task_name,
        "status": todo_doc.workflow_state,
        "task_description": todo_doc.task_description
    }
