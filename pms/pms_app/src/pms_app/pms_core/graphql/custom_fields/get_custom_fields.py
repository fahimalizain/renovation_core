from graphql import GraphQLResolveInfo
from pms_app.pms_core.controllers.custom_fields.get_custom_fields import get_custom_fields


async def get_custom_fields_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    return await get_custom_fields(
        entity_type=kwargs.get("entity_type"),
        entity=kwargs.get("entity"))
