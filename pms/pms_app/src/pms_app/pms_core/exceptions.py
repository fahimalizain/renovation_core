import renovation
from pms_app.utils import PMSException


class PMSContactNotFound(PMSException):
    def __init__(self, pms_contact: str):
        self.http_status_code = 404
        self.error_code = "PMS_CONTACT_NOT_FOUND"
        self.message = renovation._("PMS Contact not found")
        self.data = renovation._dict(
            pms_contact=pms_contact
        )


class PMSContactDisabled(PMSException):
    def __init__(self, pms_contact: str):
        self.http_status_code = 400
        self.error_code = "PMS_CONTACT_DISABLED"
        self.message = renovation._("PMS Contact has been disabled")
        self.data = renovation._dict(
            pms_contact=pms_contact
        )


class PMSContactUserUnavailable(PMSException):
    def __init__(self, pms_contact: str):
        self.http_status_code = 400
        self.error_code = "PMS_CONTACT_USER_UNAVAILABLE"
        self.message = renovation._("PMS Contact user unavailable")
        self.data = renovation._dict(
            pms_contact=pms_contact
        )


class MissingContactInfo(PMSException):
    def __init__(self, message: str = None, data=None):
        self.http_status_code = 400
        self.error_code = "MISSING_CONTACT_INFO"
        self.message = message or renovation._(
            "Please fill out required information to make the update")
        self.data = data or renovation._dict()


class EventLogParentIsNotRootLog(PMSException):
    def __init__(self, current_log: str, parent_log: str, grand_parent_log: str):
        self.http_status_code = 400
        self.error_code = "EVENT_LOG_PARENT_IS_NOT_ROOT_LOG"
        self.message = renovation._("Event Log parent should be the root log")
        self.data = renovation._dict(
            current_log=current_log,
            parent_log=parent_log,
            grand_parent_log=grand_parent_log
        )


class PrimaryEventLogCanOnlyBeSetOnRootLog(PMSException):
    def __init__(self, current_log: str, primary_log: str):
        self.http_status_code = 400
        self.error_code = "PRIMARY_EVENT_LOG_CAN_ONLY_BE_SET_ON_ROOT_LOG"
        self.message = renovation._("Primary Event Log can only be set on Root Log")
        self.data = renovation._dict(
            current_log=current_log,
            primary_log=primary_log
        )


class PrimaryEventLogDoNotBelongToCurrentThread(PMSException):
    def __init__(self, current_root: str, primary_log: str, primary_log_root: str):
        self.http_status_code = 400
        self.error_code = "PRIMARY_EVENT_LOG_DO_NOT_BELONG_TO_CURRENT_THREAD"
        self.message = renovation._("Primary Event Log do not belong to current thread")
        self.data = renovation._dict(
            current_root=current_root,
            primary_log=primary_log, primary_log_root=primary_log_root
        )


class OnlyLastEventCanBeDeleted(PMSException):
    def __init__(self, list_of_events):
        self.http_status_code = 400
        self.error_code = "ONLY_LAST_EVENT_CAN_BE_DELETED"
        self.message = renovation._("Only the last event can be deleted")
        self.data = renovation._dict(
            list_of_events=list_of_events
        )


class OnlyTheCreatorCanDeleteEventLog(PMSException):
    def __init__(self, created_by: str, current_pms_contact: str):
        self.http_status_code = 400
        self.error_code = "ONLY_THE_CREATOR_CAN_DELETE_EVENT_LOG"
        self.message = renovation._("Only creator can delete EventLog")
        self.data = renovation._dict(
            created_by=created_by,
            current_pms_contact=current_pms_contact,
        )
