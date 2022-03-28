from graphql import GraphQLResolveInfo
from pms_app.pms_core.controllers.custom_fields.get_custom_field_values_for import \
    get_custom_field_values_for


async def get_custom_field_values_for_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    return await get_custom_field_values_for(
        entity_type=kwargs.get("entity_type"),
        entity=kwargs.get("entity"))
