from graphql import GraphQLResolveInfo
from pms_app.properties.controllers.unit import delete_unit
from pms_app.utils.exceptions import PMSGQLException


@PMSGQLException
async def unit_delete_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    return await delete_unit(kwargs.get("name"))
