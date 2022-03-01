from renovation.utils.fsm import StatusBase


class PaymentWorkflowStatus(StatusBase):
    NAME = "Payment"
    # Define the states as constants
    NOT_CHARGED = 'Not Charged'
    PARTIALLY_CHARGED = 'Partially Charged'
    FULLY_CHARGED = 'Fully Charged'

    # Give the states a human readable label
    STATE_CHOICES = (
        (NOT_CHARGED, 'Not Charged'),
        (PARTIALLY_CHARGED, 'Partially Charged'),
        (FULLY_CHARGED, 'Fully Charged'),
    )

    # Define the transitions as constants
    MARK_AS_PAID = '_mark_as_paid'

    # Give the transitions a human readable label
    TRANSITION_LABELS = {
        MARK_AS_PAID: {'label': 'Mark order as paid'}
    }

    # Construct the values to pass to the state machine constructor

    # The states of the machine
    SM_STATES = [
        NOT_CHARGED, PARTIALLY_CHARGED, FULLY_CHARGED
    ]

    # The machines initial state
    SM_INITIAL_STATE = NOT_CHARGED

    # Conditions
    IS_FULLY_CHARGED = "is_fully_charged"

    # After Callbacks
    SUBMIT_ORDER = "submit_order"

    # The transitions as a list of dictionaries
    SM_TRANSITIONS = [
        # trigger, source, destination
        {
            'trigger': MARK_AS_PAID,
            'source': NOT_CHARGED,
            'dest': PARTIALLY_CHARGED,
        },
        {
            'trigger': MARK_AS_PAID,
            'source': [NOT_CHARGED, PARTIALLY_CHARGED],
            'dest': FULLY_CHARGED,
            'after': SUBMIT_ORDER,
            'conditions': IS_FULLY_CHARGED
        },
    ]


class OrderWorkflowStatus(StatusBase):
    NAME = "Order"
    # Define the states as constants
    DRAFT = 'Draft'
    UNCONFIRMED = 'Unconfirmed'
    UNFULFILLED = 'Unfulfilled'
    FULFILLED = 'Fulfilled'
    CANCELLED = 'Cancelled'

    # Give the states a human readable label
    STATE_CHOICES = (
        (DRAFT, 'Editable Order'),
        (UNCONFIRMED, 'Unconfirmed Order'),
        (UNFULFILLED, 'Unfulfilled Order'),
        (FULFILLED, 'Fulfilled Order'),
        (CANCELLED, 'Cancelled Order'),
    )

    # Define the transitions as constants
    CONFIRM_ORDER = '_confirm_order'
    SUBMIT_ORDER = '_submit_order'
    FULFILL_ORDER = '_fulfill_order'
    CANCEL_ORDER = '_cancel_order'
    START_ORDER_PAYMENT = '_start_order_payment'

    # Give the transitions a human readable label
    TRANSITION_LABELS = {
        CONFIRM_ORDER: {'label': 'Confirm order'},
        SUBMIT_ORDER: {'label': 'Submit An Order'},
        FULFILL_ORDER: {'label': 'Fulfill an Order'},
        CANCEL_ORDER: {'label': 'Cancel an Order'},
    }

    # Construct the values to pass to the state machine constructor

    # The states of the machine
    SM_STATES = [
        DRAFT,
        {
            'name': PaymentWorkflowStatus.NAME,
            'states': PaymentWorkflowStatus.SM_STATES,
            'transitions': PaymentWorkflowStatus.SM_TRANSITIONS,
            'initial': PaymentWorkflowStatus.SM_INITIAL_STATE
        },
        UNCONFIRMED,
        UNFULFILLED,
        FULFILLED,
        CANCELLED
    ]

    # The machines initial state
    SM_INITIAL_STATE = DRAFT

    # The transitions as a list of dictionaries
    SM_TRANSITIONS = [
        # trigger, source, destination
        {
            'trigger': START_ORDER_PAYMENT,
            'source': DRAFT,
            'dest': PaymentWorkflowStatus.NAME,
        },
        {
            'trigger': SUBMIT_ORDER,
            'source': f"{PaymentWorkflowStatus.NAME}_{PaymentWorkflowStatus.FULLY_CHARGED}",
            'dest': UNCONFIRMED,
        },
        {
            'trigger': CONFIRM_ORDER,
            'source': UNCONFIRMED,
            'dest': UNFULFILLED,
        },
        {
            'trigger': FULFILL_ORDER,
            'source': UNFULFILLED,
            'dest': FULFILLED
        },
        {
            'trigger': CANCEL_ORDER,
            'source': [UNCONFIRMED, UNFULFILLED, FULFILLED],
            'dest': CANCELLED,
        },
    ]
