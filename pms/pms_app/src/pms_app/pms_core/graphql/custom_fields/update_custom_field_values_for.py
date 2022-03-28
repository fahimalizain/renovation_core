from graphql import GraphQLResolveInfo
from pms_app.pms_core.controllers.custom_fields.update_custom_value_for import \
    update_custom_values_for


async def update_custom_field_values_for_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    return await update_custom_values_for(
        entity_type=kwargs.get("entity_type"),
        entity=kwargs.get("entity"),
        values=kwargs.get("values"))
