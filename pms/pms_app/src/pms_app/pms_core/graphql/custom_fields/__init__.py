from graphql import GraphQLSchema

from .get_custom_fields import get_custom_fields_resolver
from .get_customizable_entity_types import get_customizable_entity_types_resolver

from .create_custom_field import create_custom_field_resolver
from .update_custom_field import update_custom_field_resolver
from .delete_custom_field import delete_custom_field_resolver


def bind_resolvers(schema: GraphQLSchema):
    schema.query_type.fields["CustomFieldsGet"].resolve = get_custom_fields_resolver
    schema.query_type.fields["CustomFieldGetCustomizableEntityTypes"].resolve = \
        get_customizable_entity_types_resolver

    schema.mutation_type.fields["CustomFieldCreate"].resolve = create_custom_field_resolver
    schema.mutation_type.fields["CustomFieldUpdate"].resolve = update_custom_field_resolver
    schema.mutation_type.fields["CustomFieldDelete"].resolve = delete_custom_field_resolver
