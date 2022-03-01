import importlib
import os


# At this point we still haven't worked exactly what our Renovation Fields
# or Renovation Doc/Object will look like. So for now, this function assumes
# an object will be passed in that will have the following fields:

# name -> name of doctype
# fields -> list of fields to generate


def generate_controller_for_model(model, target_module):
    """
    Generate the `[model].py` and `[model]_fields.py` in [app]/models/[model]/
    """

    model_types_file_name = model.name.lower() + "_fields.py"

    renovation_app_module = importlib.import_module(target_module)
    file_path = renovation_app_module.__file__
    path_to_module = os.path.dirname(file_path)

    path_to_file = os.path.join(path_to_module, "models", model.name.lower(), model_types_file_name)

    # If it does not already exist, create it
    os.makedirs(os.path.dirname(path_to_file), exist_ok=True)

    with open(path_to_file, "w") as file:

        # Generate the class, inside it the fields and their types
        generated_code = generate_model_types(model)

        file.write(generated_code)

    model_file_name = model.name.lower() + ".py"
    path_to_file = os.path.join(path_to_module, "models", model.name.lower(), model_file_name)

    with open(path_to_file, "w") as file:

        # Generate the class etc
        generated_code = make_mode_file(model)

        file.write(generated_code)


def generate_model_types(model):
    """Use the model object to generate the Fields class and all the fields"""

    # TODO Actually implement the below steps...

    # Get all the fields

    # name, type, mandatory-ness and default value will be taken into account (pydnatic style?)

    # Put it all together and return...

    return f"class {model.name}Fields():\n    # Imagine the fields are here\n    pass\n"


def make_mode_file(model):
    """"""

    return f"""
from renovation import RenovationModel
from .{model.name.lower()}_fields import {model.name}Fields


class {model.name}(RenovationModel["{model.name}"], {model.name}Fields):
    # business logic will go here
    pass
"""
