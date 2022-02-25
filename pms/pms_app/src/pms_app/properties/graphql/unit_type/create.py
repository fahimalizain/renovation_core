from graphql import GraphQLResolveInfo
from pms_app.properties.controllers.unit_type import create_unit_type
from pms_app.utils.exceptions import PMSGQLException


@PMSGQLException
async def unit_type_create_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    return await create_unit_type(**kwargs.get("input"))
