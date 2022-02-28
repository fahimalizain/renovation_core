from graphql import GraphQLResolveInfo
from pms_app.properties.controllers.unit import create_unit
from pms_app.utils.exceptions import PMSGQLException


@PMSGQLException
async def unit_create_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    return await create_unit(**kwargs.get("input"))
