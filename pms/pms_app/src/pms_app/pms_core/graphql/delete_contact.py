from graphql import GraphQLResolveInfo

from pms_app.pms_core.controllers.contact import delete_contact
from pms_app.utils import PMSException


async def delete_contact_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    try:
        await delete_contact(pms_contact=kwargs.get("name"))
        return "SUCCESS"
    except PMSException as e:
        raise e.as_gql_error()
