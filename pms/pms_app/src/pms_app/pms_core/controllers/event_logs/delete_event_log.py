from pms_app.pms_core import PMSContactNotFound
from pms_app.pms_core.models import EventLog
from pms_app.utils import get_current_pms_contact


async def delete_event_log(event_log: str):
    """
    Deletes specified event_log

    Parameters:
        event_log (str): The name of the event log to delete

    Returns:
        deleted_successfully (bool): Returns True when delete was smooth

    Raises:
        OnlyLastEventCanBeDeleted: When the event-log being deleted is not the last in thread
        OnlyTheCreatorCanDeleteEventLog: When someone other than the creator tries to delete
    """
    contact = await get_current_pms_contact()
    if not contact:
        raise PMSContactNotFound(pms_contact=None)

    log = await EventLog.get_doc(event_log)

    await log.delete(ignore_permissions=True)

    return True
