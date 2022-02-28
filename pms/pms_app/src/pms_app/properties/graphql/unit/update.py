from graphql import GraphQLResolveInfo
from pms_app.properties.controllers.unit import update_unit
from pms_app.utils.exceptions import PMSGQLException


@PMSGQLException
async def unit_update_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    return await update_unit(kwargs.get("name"), kwargs.get("input"))
