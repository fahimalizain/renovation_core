
from pms_app.pms_core.models.pms_contact.pms_contact import PMSContact
from renovation import RenovationModel

from pms_app.pms_core import (
    PMSContactDisabled,
    PMSContactUserUnavailable,
    OnlyLastEventCanBeDeleted,
    OnlyTheCreatorCanDeleteEventLog,
    EventLogParentIsNotRootLog,
    PrimaryEventLogCanOnlyBeSetOnRootLog,
    PrimaryEventLogDoNotBelongToCurrentThread)
from pms_app.utils import get_current_pms_contact
from .event_log_types import EventLogMeta


class EventLog(RenovationModel["EventLog"], EventLogMeta):
    async def validate(self):
        await self.validate_pms_contact()
        await self.validate_parent_log()
        await self.validate_primary_log()

    async def on_trash(self):
        # Make sure this is the last thread
        if self.parent_log:
            thread_logs = await EventLog.get_all(
                {"parent_log": self.parent_log}, order_by="creation asc")
            if thread_logs[-1].name != self.name:
                raise OnlyLastEventCanBeDeleted(list_of_events=[x.name for x in thread_logs])

        # Make sure only the creator can delete
        current_contact = await get_current_pms_contact()
        if not current_contact or current_contact.name != self.created_by:
            raise OnlyTheCreatorCanDeleteEventLog(
                created_by=self.created_by,
                current_pms_contact=current_contact.name if current_contact else None
            )

        # Make sure this is not set as Primary anywhere else
        dependant_logs = await EventLog.get_all({"primary_log": self.name})
        for log in dependant_logs:
            await EventLog.db_set_value(log.name, "primary_log", None)

    async def validate_pms_contact(self):
        pms_contact = await PMSContact.get_doc(self.created_by)
        if not pms_contact.enabled:
            raise PMSContactDisabled(pms_contact=self.created_by)

        if not pms_contact.user:
            raise PMSContactUserUnavailable(pms_contact=pms_contact)

    async def validate_parent_log(self):
        if not self.parent_log:
            return
        parent_log = await EventLog.get_doc(self.parent_log)
        if parent_log.parent_log:
            raise EventLogParentIsNotRootLog(
                current_log=self.name,
                parent_log=self.parent_log,
                grand_parent_log=parent_log.parent_log)

    async def validate_primary_log(self):
        if not self.primary_log:
            return

        if self.parent_log:
            raise PrimaryEventLogCanOnlyBeSetOnRootLog(
                current_log=self.name, primary_log=self.primary_log
            )

        primary_log = await EventLog.get_doc(self.primary_log)
        if primary_log.parent_log != self.name:
            raise PrimaryEventLogDoNotBelongToCurrentThread(
                current_root=self.name,
                primary_log=self.primary_log,
                primary_log_root=primary_log.parent_log
            )
