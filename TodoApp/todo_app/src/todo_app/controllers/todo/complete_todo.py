from todo_app.models.todo_workflow import TodoTaskWorkflow


async def complete_todo(todo_name):
    todo_doc = await TodoTaskWorkflow.get_doc(todo_name)
    todo_doc.make_completed()
    todo_doc = await todo_doc.save()
    return {
        "name": todo_doc.name,
        "task_name": todo_doc.task_name,
        "status": todo_doc.workflow_state,
        "task_description": todo_doc.task_description
    }
