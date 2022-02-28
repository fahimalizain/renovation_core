from graphql import GraphQLResolveInfo
from pms_app.properties.controllers.property import delete_property
from pms_app.utils.exceptions import PMSGQLException


@PMSGQLException
async def property_delete_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    return await delete_property(kwargs.get("name"))
