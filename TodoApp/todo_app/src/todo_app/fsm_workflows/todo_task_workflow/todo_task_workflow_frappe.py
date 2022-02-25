import frappe
from todo_app.fsm_workflows.todo_task_workflow.todo_task_workflow_status_base import \
    ToDoTaskWorkflowStatus
from renovation.utils.fsm import FrappeDocumentFSM
from transitions import Machine


class ToDoTaskWorkflowMachineMixin(FrappeDocumentFSM):
    """
    Define all FSM related configurations here
    """
    status_class = ToDoTaskWorkflowStatus

    def __init__(self, *args, **kwargs):
        super(ToDoTaskWorkflowMachineMixin, self).__init__(*args, **kwargs)
        self.machine = Machine(
            model=None,
            initial=self.wf_state or self.status_class.SM_INITIAL_STATE,
            finalize_event='wf_finalize',
            auto_transitions=False,
            **self.status_class.get_kwargs()  # noqa: C815
        )

    @property
    def state(self):
        """Get the items workflow state or the initial state if none is set."""
        return self.wf_state or self.machine.initial

    @state.setter
    def state(self, value):
        """Set the items workflow state."""
        self.wf_state = value

    def wf_finalize(self, *args, **kwargs):
        """Run this on all transitions."""
        self.wf_date = frappe.utils.now()
