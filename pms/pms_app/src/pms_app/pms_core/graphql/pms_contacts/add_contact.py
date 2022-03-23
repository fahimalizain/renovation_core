from graphql import GraphQLResolveInfo

import renovation
from ..utils import get_contact_type_from_enum
from pms_app.pms_core.controllers.contact import add_contact
from pms_app.utils import PMSException


async def add_contact_resolver(obj, info: GraphQLResolveInfo, **kwargs):
    data = renovation._dict(kwargs.get("data"))

    if data.get("contact_type"):
        data["contact_type"] = get_contact_type_from_enum(data.get("contact_type"))

    try:
        pms_contact = await add_contact(data=data)
        pms_contact.__ignore_perms = 1
        return pms_contact
    except PMSException as e:
        raise e.as_gql_error()
