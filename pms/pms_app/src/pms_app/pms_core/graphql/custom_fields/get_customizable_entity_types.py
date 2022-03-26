from graphql import GraphQLResolveInfo
from pms_app.pms_core.controllers.custom_fields.get_customizable_entity_types import \
    get_customizable_entity_types


async def get_customizable_entity_types_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    return await get_customizable_entity_types()
