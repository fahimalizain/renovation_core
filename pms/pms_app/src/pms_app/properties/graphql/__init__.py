from graphql import GraphQLSchema


def bind_resolvers(schema: GraphQLSchema):
    from .unit_type import bind_resolvers as bind_unit_type_resolvers
    bind_unit_type_resolvers(schema)
