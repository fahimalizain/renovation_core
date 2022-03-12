from enum import Enum

from renovation import RenovationModel, _dict
from .event_type_types import EventTypeMeta


class EventType(RenovationModel["EventType"], EventTypeMeta):
    pass


class EventTypes(Enum):
    CONCERN = "Concern"
    MESSAGE = "Message"
    MAINTENANCE_REQUEST = "MAINTENANCE_REQUEST"
    FINE_CHARGED = "Fine Charged"
    INVOICE_GENERATED = "Invoice Generated"
    PAYMENT_MADE = "Payment Made"


async def make_default_event_types():
    types = [
        _dict(
            title=EventTypes.CONCERN,
            actions=["MAKE_MAINTENANCE_REQUEST", "MAKE_EXPENSE_ENTRY", "MAKE_TENANT_FINE"]
        ),
        _dict(
            title=EventTypes.MESSAGE, actions=[],
        ),
        _dict(
            title=EventTypes.MAINTENANCE_REQUEST,
            actions=["ACTIONS_ON_MAINTENANCE_REQUEST"]
        ),
        _dict(
            title=EventTypes.FINE_CHARGED,
            actions=["MAKE_PAYMENT"]
        ),
        _dict(
            title=EventTypes.INVOICE_GENERATED,
            actions=["MAKE_PAYMENT", "SEND_REMINDER"]
        ),
        _dict(
            title=EventTypes.PAYMENT_MADE,
            actions=["SEND_RECEIPT"]
        ),
    ]

    docs = []
    for t in types:
        title = t.title.value
        if await EventType.exists(title):
            d = await EventType.get_doc(title)
        else:
            d = EventType(_dict(title=t.title.value,))

        d.actions = "\n".join(t.actions or [])
        await d.save()
        docs.append(d)

    return docs
