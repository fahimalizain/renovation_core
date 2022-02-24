from frappe.model.document import Document
from renovation.base_transitions import StateMachineMixinBase


class FrappeDocumentFSM(Document, StateMachineMixinBase):
    """
    The field name of the workflow_state & workflow_date
    The Document will be tracked by the workflow state and workflow date will contain the datetime
    value of the when the workflow status changed last.
    """
    wf_state = None  # override this
    wf_date = None  # override this
