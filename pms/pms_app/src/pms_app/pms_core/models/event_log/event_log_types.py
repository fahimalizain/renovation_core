from typing import Optional


class EventLogMeta:
    entity_type: str
    entity: str
    created_by: str
    parent_log: Optional[str]
    primary_log: Optional[str]
    event_type: str
    ref_dt: Optional[str]
    ref_dn: Optional[str]
    attachment: Optional[str]
    content: Optional[str]
