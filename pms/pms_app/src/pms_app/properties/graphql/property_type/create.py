from graphql import GraphQLResolveInfo
from pms_app.properties.controllers.property_type import create_property_type
from pms_app.utils.exceptions import PMSGQLException


@PMSGQLException
async def property_type_create_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    return await create_property_type(**kwargs.get("input"))
