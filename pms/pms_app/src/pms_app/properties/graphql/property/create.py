from graphql import GraphQLResolveInfo
from pms_app.properties.controllers.property import create_property
from pms_app.utils.exceptions import PMSGQLException


@PMSGQLException
async def property_create_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    return await create_property(**kwargs.get("input"))
