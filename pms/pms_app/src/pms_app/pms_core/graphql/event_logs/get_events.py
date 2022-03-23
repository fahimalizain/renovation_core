from graphql import GraphQLResolveInfo
from ...controllers.event_logs.get_events import get_events


async def get_events_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    return await get_events(model=kwargs.get("model"), name=kwargs.get("name"))
