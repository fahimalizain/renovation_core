import os
from typing import Generator
import graphql
from graphql import GraphQLError, parse, GraphQLSyntaxError

import frappe


async def execute(query=None, variables=None, operation_name=None):
    result = await graphql.graphql(
        # is_awaitable=is_awaitable,
        schema=get_schema(),
        source=query,
        variable_values=variables,
        operation_name=operation_name,
        middleware=[frappe.get_attr(cmd) for cmd in frappe.get_hooks("graphql_middlewares")],
        context_value=frappe._dict()
    )
    output = frappe._dict()
    for k in ("data", "errors"):
        if not getattr(result, k, None):
            continue
        output[k] = getattr(result, k)
    return output


def log_error(query, variables, operation_name, output):
    import traceback as tb
    tracebacks = []
    for idx, err in enumerate(output.errors):
        if not isinstance(err, GraphQLError):
            continue

        exc = err.original_error
        if not exc:
            continue
        tracebacks.append(
            f"GQLError #{idx}\n"
            + f"Http Status Code: {getattr(exc, 'http_status_code', 500)}\n"
            + f"{str(err)}\n\n"
            + f"{''.join(tb.format_exception(exc, exc, exc.__traceback__))}"
        )

    tracebacks.append(f"Frappe Traceback: \n{frappe.get_traceback()}")
    if frappe.conf.get("developer_mode"):
        frappe.errprint(tracebacks)

    tracebacks = "\n==========================================\n".join(tracebacks)
    if frappe.conf.get("developer_mode"):
        print(tracebacks)


graphql_schemas = {}


def get_schema():
    global graphql_schemas

    if frappe.local.site in graphql_schemas:
        return graphql_schemas.get(frappe.local.site)

    schema = graphql.build_schema(get_typedefs())
    execute_schema_processors(schema=schema)

    graphql_schemas[frappe.local.site] = schema
    return schema


def get_typedefs():
    target_dir = frappe.get_site_path("doctype_sdls")
    schema = load_schema_from_path(target_dir) if os.path.isdir(
        target_dir) else ""

    for dir in frappe.get_hooks("graphql_sdl_dir"):
        dir = os.path.abspath(frappe.get_app_path("frappe", "../..", dir))

        schema += f"\n\n\n# {dir}\n\n"
        schema += load_schema_from_path(dir)

    return schema


def load_schema_from_path(path: str) -> str:
    if os.path.isdir(path):
        schema_list = [read_graphql_file(f) for f in
                       sorted(walk_graphql_files(path))]
        return "\n".join(schema_list)
    return read_graphql_file(os.path.abspath(path))


def execute_schema_processors(schema):
    for cmd in frappe.get_hooks("graphql_schema_processors"):
        frappe.get_attr(cmd)(schema=schema)


def walk_graphql_files(path: str) -> Generator[str, None, None]:
    extension = ".graphql"
    for dirpath, _, files in os.walk(path):
        for name in files:
            if extension and name.lower().endswith(extension):
                yield os.path.join(dirpath, name)


def read_graphql_file(path: str) -> str:
    with open(path, "r") as graphql_file:
        schema = graphql_file.read()
    try:
        parse(schema)
    except GraphQLSyntaxError as e:
        raise GraphQLFileSyntaxError(path, str(e)) from e
    return schema


class GraphQLFileSyntaxError(Exception):
    def __init__(self, schema_file, message) -> None:
        super().__init__()
        self.message = self.format_message(schema_file, message)

    def format_message(self, schema_file, message):
        return f"Could not load {schema_file}:\n{message}"

    def __str__(self):
        return self.message
