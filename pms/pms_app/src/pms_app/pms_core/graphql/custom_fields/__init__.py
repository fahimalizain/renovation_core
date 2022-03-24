from graphql import GraphQLSchema
from .create_custom_field import create_custom_field_resolver
from .update_custom_field import update_custom_field_resolver
from .delete_custom_field import delete_custom_field_resolver


def bind_resolvers(schema: GraphQLSchema):
    schema.mutation_type.fields["CustomFieldCreate"].resolve = create_custom_field_resolver
    schema.mutation_type.fields["CustomFieldUpdate"].resolve = update_custom_field_resolver
    schema.mutation_type.fields["CustomFieldDelete"].resolve = delete_custom_field_resolver
