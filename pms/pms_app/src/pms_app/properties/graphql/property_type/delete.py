from graphql import GraphQLResolveInfo
from pms_app.properties.controllers.property_type import delete_property_type
from pms_app.utils.exceptions import PMSGQLException


@PMSGQLException
async def property_type_delete_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    if await delete_property_type(kwargs.get("name")):
        return "SUCCESS"
