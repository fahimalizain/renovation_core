from graphql import GraphQLResolveInfo
from pms_app.properties.controllers.property import update_property
from pms_app.utils.exceptions import PMSGQLException


@PMSGQLException
async def property_update_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    return await update_property(kwargs.get("name"), kwargs.get("input"))
