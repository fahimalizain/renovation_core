from pms_app.pms_core import PMSContactNotFound
from pms_app.pms_core.models import EventLog
from pms_app.utils import get_current_pms_contact

from . import EventLogData


async def create_event_log(data: EventLogData):
    contact = await get_current_pms_contact()
    if not contact:
        raise PMSContactNotFound(pms_contact=None)

    log = EventLog(data)
    log.created_by = contact.name

    await log.insert(ignore_permissions=True)

    return log
