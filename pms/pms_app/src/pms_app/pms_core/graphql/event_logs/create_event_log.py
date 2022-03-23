from graphql import GraphQLResolveInfo
from ...controllers.event_logs.create_event_log import create_event_log


async def create_event_log_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    return await create_event_log(data=kwargs.get("data"))
