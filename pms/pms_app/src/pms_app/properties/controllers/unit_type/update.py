from renovation import _
from pms_app.properties.exceptions import UnitTypeNotFound
from pms_app.properties.models.unit_type import UnitType


async def update_unit_type(name: str, input):

    if not await UnitType.exists(name):
        raise UnitTypeNotFound(message=(_("Unit Type with name '{0}' not found.")).format(name))

    doc = await UnitType.get_doc(name)

    # If any attributes were passed in, handle them
    if input.get("unit_attributes"):
        unit_attributes_input = input.get("unit_attributes")
        del input["unit_attributes"]

        doc.unit_attributes = []
        # Replace ENUM case with Title case
        for unit_attribute in unit_attributes_input:
            if unit_attribute.get("attribute_type"):
                unit_attribute["attribute_type"] = \
                    unit_attribute["attribute_type"].title().replace("_", "-")
            doc.append("unit_attributes", unit_attribute)

    doc.update(input)
    await doc.save()

    return doc
