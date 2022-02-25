import inspect
from typing import Optional

from graphql import GraphQLError
from renovation import _dict, _


def PMSGQLException(fn):
    """
    Use this function decorator to automatically map PMSException to GQLError
    """
    is_async = inspect.isawaitable(fn)

    def _inner(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except PMSException as e:
            raise e.as_gql_error()

    async def _inner_async(*args, **kwargs):
        try:
            return await fn(*args, **kwargs)
        except PMSException as e:
            raise e.as_gql_error()

    if is_async:
        return _inner_async
    else:
        return _inner


class PMSException(Exception):
    """
    PMSException Base Class
    """
    error_code: str
    message: str
    data: dict
    http_status_code: int = 500

    def __init__(self) -> None:
        super().__init__(None)

    def as_dict(self):
        return _dict(
            message=self.message,
            error_code=self.error_code,
            **self.data,
        )

    def as_gql_error(self):
        gql_error = GraphQLError(
            message=self.message,
            extensions=_dict(
                # error_code=self.error_code,
                # TODO: Find why error_code is a tuple
                error_code=self.error_code[0]
                if isinstance(self.error_code, (list, tuple)) else self.error_code,
                error_message=self.message,
                error_data=self.data,
            ))
        gql_error.http_status_code = self.http_status_code
        return gql_error


class PermissionDenied(PMSException):
    def __init__(self, message: Optional[str] = None, **data) -> None:
        self.http_status_code = 401
        self.error_code = "PERMISSION_DENIED"
        self.message = message or _("Permission Denied")
        self.data = _dict(
            **data
        )
