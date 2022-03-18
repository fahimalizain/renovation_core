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
    ADD_PAYMENT = '_add_payment'

    # Give the transitions a human readable label
    TRANSITION_LABELS = {
        ADD_PAYMENT: {'label': 'Add a payment'}
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
    IS_NOT_FULLY_CHARGED = "is_not_fully_charged"

    # After Callbacks
    SUBMIT_ORDER = "submit_order"

    # The transitions as a list of dictionaries
    SM_TRANSITIONS = [
        # trigger, source, destination
        {
            'trigger': ADD_PAYMENT,
            'source': NOT_CHARGED,
            'dest': PARTIALLY_CHARGED,
            'conditions': ['is_not_fully_charged']
        },
        {
            'trigger': ADD_PAYMENT,
            'source': [NOT_CHARGED, PARTIALLY_CHARGED],
            'dest': FULLY_CHARGED,
            'after': SUBMIT_ORDER,
            'conditions': [IS_FULLY_CHARGED]
        },
    ]


class FulfillmentLineWorkflowStatus(StatusBase):
    NAME = "FulfillmentLineStateMachine"
    # Define the states as constants
    PENDING = 'Pending'
    OUT_FOR_DELIVERY = 'Out For Delivery'
    DELIVERED = 'Delivered'

    # Give the states a human readable label
    STATE_CHOICES = (
        (PENDING, 'Pending'),
        (OUT_FOR_DELIVERY, 'Out For Delivery'),
        (DELIVERED, 'Delivered'),
    )

    # Define the transitions as constants
    ITEM_OUT_FOR_DELIVERY = '_item_out_for_delivery'
    ITEM_DELIVERED = '_item_delivered'

    # Give the transitions a human readable label
    TRANSITION_LABELS = {
        ITEM_OUT_FOR_DELIVERY: {'label': 'Item out for delivery'},
        ITEM_DELIVERED: {'label': 'Item delivered'}
    }

    # Construct the values to pass to the state machine constructor

    # The states of the machine
    SM_STATES = [
        PENDING, OUT_FOR_DELIVERY, DELIVERED
    ]

    # The machines initial state
    SM_INITIAL_STATE = PENDING

    # The transitions as a list of dictionaries
    SM_TRANSITIONS = [
        # trigger, source, destination
        {
            'trigger': ITEM_OUT_FOR_DELIVERY,
            'source': PENDING,
            'dest': OUT_FOR_DELIVERY,
        },
        {
            'trigger': ITEM_DELIVERED,
            'source': OUT_FOR_DELIVERY,
            'dest': DELIVERED,
        },
    ]


class OrderWorkflowStatus(StatusBase):
    NAME = "Order"
    # Define the states as constants
    DRAFT = 'Draft'
    UNCONFIRMED = 'Unconfirmed'
    UNFULFILLED = 'Unfulfilled'
    FULFILLED = 'Fulfilled'
    PARTIALLY_FULFILLED = 'Partially Fulfilled'
    CANCELLED = 'Cancelled'

    # Give the states a human readable label
    STATE_CHOICES = (
        (DRAFT, 'Editable Order'),
        (UNCONFIRMED, 'Unconfirmed Order'),
        (UNFULFILLED, 'Unfulfilled Order'),
        (PARTIALLY_FULFILLED, 'Partially Fulfilled'),
        (FULFILLED, 'Fulfilled Order'),
        (CANCELLED, 'Cancelled Order'),
    )

    # Define the transitions as constants
    CONFIRM_ORDER = '_confirm_order'
    SUBMIT_ORDER = '_submit_order'
    FULFILL_ORDER = '_fulfill_order'
    AFTER_ORDER_FULFILL = 'after_order_fulfill'
    CREATE_FULFILLMENT_LINES = 'create_fulfillment_lines'
    ORDER_FULFILLED = '_order_fulfilled'
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
        {
            'name': FulfillmentLineWorkflowStatus.NAME,
            'states': FulfillmentLineWorkflowStatus.SM_STATES,
            'transitions': FulfillmentLineWorkflowStatus.SM_TRANSITIONS,
            'initial': FulfillmentLineWorkflowStatus.SM_INITIAL_STATE
        },
        PARTIALLY_FULFILLED,
        FULFILLED,
        CANCELLED
    ]

    # The machines initial state
    SM_INITIAL_STATE = DRAFT

    # Conditions
    IS_ALL_ITEMS_FULFILLED = "is_all_items_fulfilled"
    IS_ALL_ITEMS_NOT_FULFILLED = "is_all_items_not_fulfilled"

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
            'before': CREATE_FULFILLMENT_LINES,
            'source': UNFULFILLED,
            'after': AFTER_ORDER_FULFILL,
            'dest': f"{FulfillmentLineWorkflowStatus.NAME}_{FulfillmentLineWorkflowStatus.PENDING}"
        },

        {
            'trigger': ORDER_FULFILLED,
            'source': f"{FulfillmentLineWorkflowStatus.NAME}_{FulfillmentLineWorkflowStatus.DELIVERED}",
            'dest': PARTIALLY_FULFILLED,
            "conditions": IS_ALL_ITEMS_NOT_FULFILLED
        },
        {
            'trigger': ORDER_FULFILLED,
            'source': [
                f"{FulfillmentLineWorkflowStatus.NAME}_{FulfillmentLineWorkflowStatus.DELIVERED}",
                PARTIALLY_FULFILLED],
            'dest': FULFILLED,
            'conditions': IS_ALL_ITEMS_FULFILLED
        },
        {
            'trigger': CANCEL_ORDER,
            'source': [UNCONFIRMED, UNFULFILLED, FULFILLED],
            'dest': CANCELLED,
        },
    ]
