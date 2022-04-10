from graphql import parse

import renovation


def get_masked_variables(query, variables):
    """
    Return the variables dict with password field set to "******"
    """
    if isinstance(variables, str):
        variables = renovation.parse_json(variables)

    variables = renovation._dict(variables)
    try:
        document = parse(query)
        for operation_definition in (getattr(document, "definitions", None) or []):
            for variable in (getattr(operation_definition, "variable_definitions", None) or []):
                variable_name = variable.variable.name.value
                variable_type = variable.type

                if variable_name not in variables:
                    continue

                if not isinstance(variables[variable_name], str):
                    continue

                # Password! NonNull
                if variable_type.kind == "non_null_type":
                    variable_type = variable_type.type

                # Password is a named_type
                if variable_type.kind != "named_type" or not variable_type.name:
                    continue

                if variable_type.name.value != "Password":
                    continue

                variables[variable_name] = "*" * len(variables[variable_name])
    except BaseException:
        return renovation._dict(
            status="Error Processing Variable Definitions",
            traceback=renovation.get_traceback()
        )

    return variables


def get_operation_name(query, operation_name):
    """
    Gets the active operation name
    if operation_name is not specified in the request,
    it will take on the first operation definition if available.
    Otherwise returns 'unnamed-query'
    """
    defined_operations = []
    try:
        document = parse(query)
        for operation_definition in document.definitions:
            if operation_definition.kind != "operation_definition":
                continue

            # For non-named Queries
            if not operation_definition.name:
                continue

            defined_operations.append(operation_definition.name.value)
    except BaseException:
        pass

    if not operation_name and len(defined_operations):
        return defined_operations[0]
    elif operation_name in defined_operations:
        return operation_name
    elif operation_name:
        return f"{operation_name} (invalid)"
    else:
        return "unnamed-query"
