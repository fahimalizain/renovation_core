from graphql import GraphQLResolveInfo
from ...controllers.event_logs.get_event_types import get_event_types


async def get_event_types_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    return await get_event_types(model=kwargs.get("model"))
