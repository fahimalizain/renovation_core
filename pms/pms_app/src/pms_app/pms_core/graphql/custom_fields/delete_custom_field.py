from graphql import GraphQLResolveInfo
from pms_app.pms_core.controllers.custom_fields.delete_custom_field import delete_custom_field


async def delete_custom_field_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    return await delete_custom_field(
        custom_field=kwargs.get("custom_field"))
