from renovation.utils.fsm.check_if_valid_transition import check_if_valid_transition
from todo_app.fsm_workflows.todo_task_workflow.todo_task_workflow_frappe import \
    ToDoTaskWorkflowMachineMixin
from renovation import RenovationModel
from todo_app.fsm_workflows.todo_task_workflow.todo_task_workflow_status_base import \
    ToDoTaskWorkflowStatus


class TodoTaskWorkflow(RenovationModel["ToDoWorkflow"], ToDoTaskWorkflowMachineMixin):
    wf_state = "workflow_state"
    wf_date = "workflow_date"

    """
    Define the triggers that are called on state change
    """

    def activate_todo(self):
        """
        Why doesnt the following work? 🤔
        self.machine.dispatch("activate_todo")
        """
        self._activate_todo()

    def make_completed(self):
        self._make_completed()

    def mark_deleted(self):
        self._mark_deleted()

    def revert_delete(self):
        self._revert_delete()

    @check_if_valid_transition(field_name="workflow_state", status=ToDoTaskWorkflowStatus.DRAFT)
    async def edit_todo(self, task_description=None, task_name=None):
        self.update({"task_description": task_description, "task_name": task_name})
        await self.save()
