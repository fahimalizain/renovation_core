from graphql import GraphQLResolveInfo
from pms_app.pms_core.controllers.auth.get_bearer_token_with_refresh_token import \
    get_bearer_token_with_refresh_token


async def token_refresh_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    return await get_bearer_token_with_refresh_token(
        refresh_token=kwargs.get("refreshToken")
    )
