from graphql import GraphQLResolveInfo
from pms_app.pms_core.controllers.auth.get_bearer_token_with_password import \
    get_bearer_token_with_password


async def token_create_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    return await get_bearer_token_with_password(
        email=kwargs.get("email"),
        pwd=kwargs.get("password")
    )
