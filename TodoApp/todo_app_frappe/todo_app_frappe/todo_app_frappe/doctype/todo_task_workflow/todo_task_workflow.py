# Copyright (c) 2022, LEAM and contributors
# For license information, please see license.txt


from todo_app.models.todo_workflow import TodoTaskWorkflow as _TodoTaskWorkflow
from renovation.model import map_doctype

map_doctype("Todo Task Workflow", _TodoTaskWorkflow)


class TodoTaskWorkflow(_TodoTaskWorkflow):
    pass
