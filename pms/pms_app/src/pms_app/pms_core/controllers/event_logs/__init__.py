import renovation
from typing import TypedDict


class EventLogData(renovation._dict, TypedDict):
    entity: str
    entity_type: str
    event_type: str
    ref_dt: str
    ref_dn: str
    attachment: str
    content: str
