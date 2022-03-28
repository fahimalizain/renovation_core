from unittest import TestCase
from asyncer import runnify
from pms_app.pms_core.models.pms_custom_field.pms_custom_field import PMSCustomField
import renovation

from ..get_custom_field_values_for import get_custom_field_values_for
from pms_app.pms_core.models.pms_custom_field.test_pms_custom_field import PMSCustomFieldTestFixture
from pms_app.pms_core.models.pms_custom_field_value.test_pms_custom_field_value import \
    PMSCustomFieldValueFixtures


class TestGetCustomFieldValuesFor(TestCase):
    custom_fields = PMSCustomFieldTestFixture()
    custom_field_values = PMSCustomFieldValueFixtures()

    @classmethod
    @runnify
    async def setUpClass(cls):
        await cls.custom_fields.setUp()
        await cls.custom_field_values.setUp()

    @classmethod
    @runnify
    async def tearDownClass(cls):
        await cls.custom_field_values.tearDown()
        await cls.custom_fields.tearDown()

    @runnify
    async def test_simple(self):
        cf_value = self.custom_field_values[0]
        values = await get_custom_field_values_for(cf_value.entity_type, cf_value.entity)

        self.assertEqual(values.get(cf_value.fieldname), await cf_value.get_parsed_value())

    @runnify
    async def test_integer(self):
        cf_integer: PMSCustomField = [x for x in self.custom_fields if x.fieldtype == "Integer"][0]
        entity_type = "PMS Contact"

        values = await get_custom_field_values_for(
            entity_type, renovation.local.db.get_value(entity_type, dict()))

        self.assertIsInstance(values.get(cf_integer.fieldname), int)

    @runnify
    async def test_float(self):
        cf_integer: PMSCustomField = [x for x in self.custom_fields if x.fieldtype == "Float"][0]
        entity_type = "PMS Contact"

        values = await get_custom_field_values_for(
            entity_type, renovation.local.db.get_value(entity_type, dict()))

        self.assertIsInstance(values.get(cf_integer.fieldname), float)
