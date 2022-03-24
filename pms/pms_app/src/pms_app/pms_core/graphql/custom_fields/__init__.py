from graphql import GraphQLSchema
from .create_custom_field import create_custom_field_resolver


def bind_resolvers(schema: GraphQLSchema):
    schema.mutation_type.fields["CustomFieldCreate"].resolve = create_custom_field_resolver
