from graphql import GraphQLResolveInfo
from pms_app.properties.controllers.property_type import update_property_type
from pms_app.utils.exceptions import PMSGQLException


@PMSGQLException
async def property_type_update_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    return await update_property_type(kwargs.get("name"), kwargs.get("input"))
