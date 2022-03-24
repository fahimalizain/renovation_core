from graphql import GraphQLResolveInfo
from pms_app.pms_core.controllers.custom_fields.create_custom_field import create_custom_field


async def create_custom_field_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    return await create_custom_field(data=kwargs.get("data"))
