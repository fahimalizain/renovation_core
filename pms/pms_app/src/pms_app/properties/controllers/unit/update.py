from renovation import _
from pms_app.properties.exceptions import UnitNotFound
from pms_app.properties.models.unit import Unit


async def update_unit(name: str, input):
    if not await Unit.exists(name):
        raise UnitNotFound(message=(_("Unit with name '{0}' not found.")).format(name))

    doc = await Unit.get_doc(name)

    # If any attributes were passed in, handle them
    if input.get("unit_attributes"):
        doc.unit_attributes = []
        unit_attributes_input = input.get("unit_attributes")
        del input["unit_attributes"]

        for unit_attribute in unit_attributes_input:
            doc.append("unit_attributes", unit_attribute)

    doc.update(input)
    await doc.save()

    return doc
