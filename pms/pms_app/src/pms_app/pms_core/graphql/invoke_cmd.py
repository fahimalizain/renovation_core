import inspect
from graphql import GraphQLResolveInfo

import renovation
from pms_app.utils.exceptions import PMSGQLException


@PMSGQLException
async def invoke_cmd_resolver(obj, info: GraphQLResolveInfo, **kwargs):

    args = renovation._dict(kwargs.get("args", {}))
    method = renovation.get_attr(kwargs.get("cmd"))
    renovation.is_whitelisted(method)

    if inspect.iscoroutinefunction(method):
        return await method(**args)
    else:
        return method(**args)
