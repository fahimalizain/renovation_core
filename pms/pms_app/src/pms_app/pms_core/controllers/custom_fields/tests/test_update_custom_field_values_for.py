from unittest import TestCase
from asyncer import runnify

from ..update_custom_value_for import update_custom_values_for
from pms_app.pms_core.models.pms_custom_field.pms_custom_field import PMSCustomField
from pms_app.pms_core.models.pms_custom_field.test_pms_custom_field import PMSCustomFieldTestFixture
from pms_app.properties.models.unit.test_unit import UnitFixtures


class TestUpdateCustomFieldValuesFor(TestCase):
    custom_fields = PMSCustomFieldTestFixture()
    units = UnitFixtures()

    @classmethod
    @runnify
    async def setUpClass(cls):
        await cls.units.setUp()
        await cls.custom_fields.setUp()

    @classmethod
    @runnify
    async def tearDownClass(cls):
        await cls.custom_fields.tearDown()
        await cls.units.tearDown()

    @runnify
    async def test_simple(self):
        cf_data = [x for x in self.custom_fields if x.fieldtype == "Data"][0]
        unit1 = self.units[0]

        new_value = "RANDOM_NEW_VALUE"
        values = await update_custom_values_for(unit1.get_doctype(), unit1.name, {
            cf_data.fieldname: new_value
        })

        self.assertEqual(values.get(cf_data.fieldname), new_value)

    @runnify
    async def test_integer(self):
        cf_integer: PMSCustomField = [x for x in self.custom_fields if x.fieldtype == "Integer"][0]
        unit1 = self.units[0]

        new_value = 12
        values = await update_custom_values_for(
            unit1.get_doctype(), unit1.name, {
                cf_integer.fieldname: new_value
            })

        self.assertEqual(values.get(cf_integer.fieldname), new_value)
        self.assertIsInstance(values.get(cf_integer.fieldname), int)

    @runnify
    async def test_float(self):
        cf_float: PMSCustomField = [x for x in self.custom_fields if x.fieldtype == "Float"][0]
        unit1 = self.units[0]

        new_value = 12.5
        values = await update_custom_values_for(
            unit1.get_doctype(), unit1.name, {
                cf_float.fieldname: new_value
            })

        self.assertEqual(values.get(cf_float.fieldname), new_value)
        self.assertIsInstance(values.get(cf_float.fieldname), float)
