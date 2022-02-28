from graphql import GraphQLSchema


def bind_resolvers(schema: GraphQLSchema):
    from .unit_type import bind_resolvers as bind_unit_type_resolvers
    bind_unit_type_resolvers(schema)

    from .property_type import bind_resolvers as bind_property_type_resolvers
    bind_property_type_resolvers(schema)

    from .property import bind_resolvers as bind_property_resolvers
    bind_property_resolvers(schema)

    from .unit import bind_resolvers as bind_unit_resolvers
    bind_unit_resolvers(schema)
