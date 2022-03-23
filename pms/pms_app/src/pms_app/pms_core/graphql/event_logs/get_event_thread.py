from graphql import GraphQLResolveInfo
from ...controllers.event_logs.get_event_thread import get_event_thread


async def get_event_thread_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    return await get_event_thread(parent_log=kwargs.get("parent_log"))
