from todo_app.fsm_workflows.todo_task_workflow.todo_task_workflow_frappe import \
    ToDoTaskWorkflowMachineMixin
from renovation import RenovationModel


class TodoTaskWorkflow(RenovationModel["ToDoWorkflow"], ToDoTaskWorkflowMachineMixin):
    wf_state = "workflow_state"
    wf_date = "workflow_date"
