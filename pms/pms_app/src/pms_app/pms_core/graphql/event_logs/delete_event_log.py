from graphql import GraphQLResolveInfo
from ...controllers.event_logs.delete_event_log import delete_event_log


async def delete_event_log_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    return await delete_event_log(event_log=kwargs.get("event_log"))
