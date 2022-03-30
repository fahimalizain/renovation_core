from graphql import GraphQLResolveInfo
from pms_app.pms_core.controllers.auth.get_me import get_me


async def get_me_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    return await get_me()
