import frappe
from renovation.utils.fsm import FrappeDocumentFSM
from transitions.extensions import HierarchicalAsyncGraphMachine

from todo_app.fsm_workflows.order_workflow.order_workflow_status_base import OrderWorkflowStatus, \
    PaymentWorkflowStatus


class OrderWorkflowMachineMixin(FrappeDocumentFSM):
    status_class = OrderWorkflowStatus

    def __init__(self, *args, **kwargs):
        super(OrderWorkflowMachineMixin, self).__init__(*args, **kwargs)
        self.machine = HierarchicalAsyncGraphMachine(
            model=self,
            initial=self.get(self.wf_state) or self.status_class.SM_INITIAL_STATE,
            finalize_event='wf_finalize',
            auto_transitions=False,
            send_event=True,
            states=self.status_class.SM_STATES,
            transitions=self.status_class.SM_TRANSITIONS,  # noqa: C815
            show_conditions=True,
            show_state_attributes=True,
            title=self.status_class.NAME
        )
        if not self.get(self.wf_date):
            self.set(self.wf_date, frappe.utils.now())

    @property
    def state(self):
        """Get the items workflow state or the initial state if none is set."""
        return self.get(self.wf_state) or self.machine.initial

    @state.setter
    def state(self, value):
        """Set the items workflow state."""
        self.set(self.wf_state, value)

    def wf_finalize(self, *args, **kwargs):
        """Run this on all transitions."""
        self.set(self.wf_date, frappe.utils.now())


class PaymentWorkflowMachineMixin(FrappeDocumentFSM):
    status_class = PaymentWorkflowStatus

    def __init__(self, *args, **kwargs):
        super(PaymentWorkflowMachineMixin, self).__init__(*args, **kwargs)
        self.machine = HierarchicalAsyncGraphMachine(
            model=self,
            initial=self.get(self.wf_state) or self.status_class.SM_INITIAL_STATE,
            finalize_event='wf_finalize',
            auto_transitions=False,
            send_event=True,
            states=self.status_class.SM_STATES,
            show_conditions=True,
            show_state_attributes=True,
            transitions=self.status_class.SM_TRANSITIONS,
            title=self.status_class.NAME
        )
        if not self.get(self.wf_date):
            self.set(self.wf_date, frappe.utils.now())

    @property
    def state(self):
        """Get the items workflow state or the initial state if none is set."""
        return self.get(self.wf_state) or self.machine.initial

    @state.setter
    def state(self, value):
        """Set the items workflow state."""
        self.set(self.wf_state, value)

    def wf_finalize(self, *args, **kwargs):
        """Run this on all transitions."""
        self.set(self.wf_date, frappe.utils.now())
