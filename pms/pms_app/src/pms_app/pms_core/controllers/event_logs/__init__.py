import renovation
from typing import TypedDict, Optional


class EventLogData(renovation._dict, TypedDict):
    entity: str
    entity_type: str
    event_type: str
    ref_dt: str
    ref_dn: str
    attachment: str
    content: str
    parent_log: Optional[str]
