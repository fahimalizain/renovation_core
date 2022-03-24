from graphql import GraphQLResolveInfo
from pms_app.pms_core.controllers.custom_fields.update_custom_field import update_custom_field


async def update_custom_field_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    return await update_custom_field(
        custom_field=kwargs.get("custom_field"),
        data=kwargs.get("data"))
