from renovation.utils.fsm import StatusBase


class ToDoTaskWorkflowStatus(StatusBase):
    # Define the states as constants
    DRAFT = 'Draft'
    ACTIVE = 'Active'
    COMPLETED = 'Completed'
    DELETED = 'Deleted'

    # Give the states a human readable label
    STATE_CHOICES = (
        (DRAFT, 'Editable ToDo'),
        (ACTIVE, 'Active ToDo'),
        (COMPLETED, 'Completed ToDo'),
        (DELETED, 'Deleted ToDo'),
    )

    # Define the transitions as constants
    ACTIVATE = '_activate_todo'
    MARK_COMPLETED = '_make_completed'
    MARK_DELETED = '_mark_deleted'
    REVERT_DELETED = '_revert_delete'

    # Give the transitions a human readable label
    TRANSITION_LABELS = {
        ACTIVATE: {'label': 'Make ToDo active'},
        MARK_COMPLETED: {'label': 'Mark ToDo as completed'},
        MARK_DELETED: {'label': 'Mark ToDo as deleted'},
        REVERT_DELETED: {'label': 'Revert Deleted ToDo'},
    }

    # Construct the values to pass to the state machine constructor

    # The states of the machine
    SM_STATES = [
        DRAFT, ACTIVE, COMPLETED, DELETED,
    ]

    # The machines initial state
    SM_INITIAL_STATE = DRAFT

    # The transitions as a list of dictionaries
    SM_TRANSITIONS = [
        # trigger, source, destination
        {
            'trigger': ACTIVATE,
            'source': DRAFT,
            'dest': ACTIVE,
        },
        {
            'trigger': MARK_COMPLETED,
            'source': ACTIVE,
            'dest': COMPLETED,
        },
        {
            'trigger': MARK_DELETED,
            'source': [
                ACTIVE, COMPLETED, DRAFT
            ],
            'dest': DELETED
        },
        {
            'trigger': REVERT_DELETED,
            'source': DELETED,
            'dest': DRAFT,
        },
    ]
