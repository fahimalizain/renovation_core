from graphql import GraphQLResolveInfo
from pms_app.properties.controllers.unit_type import update_unit_type
from pms_app.utils.exceptions import PMSGQLException


@PMSGQLException
async def unit_type_update_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    return await update_unit_type(**kwargs)
