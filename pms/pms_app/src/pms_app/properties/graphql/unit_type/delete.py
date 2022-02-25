from graphql import GraphQLResolveInfo
from pms_app.properties.controllers.unit_type import delete_unit_type
from pms_app.utils.exceptions import PMSGQLException


@PMSGQLException
async def unit_type_delete_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    if await delete_unit_type(kwargs.get("name")):
        return "SUCCESS"
