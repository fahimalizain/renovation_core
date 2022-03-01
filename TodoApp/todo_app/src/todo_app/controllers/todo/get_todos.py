from todo_app.models.todo_workflow import TodoTaskWorkflow


async def get_todos():
    todos = await TodoTaskWorkflow.get_all(filters={},
                                           fields=["name", "task_name", "workflow_state as status",
                                                   "task_description"])
    return todos
