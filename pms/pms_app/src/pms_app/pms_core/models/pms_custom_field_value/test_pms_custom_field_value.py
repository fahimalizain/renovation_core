from unittest import TestCase
from faker import Faker
from asyncer import runnify
from pms_app.utils.exceptions import NotFound

import renovation
from renovation.tests import RenovationTestFixture

from .pms_custom_field_value import PMSCustomFieldValue
from .exceptions import CustomFieldNotApplicableOnEntityType, InvalidValueForSelectField
from ..pms_custom_field.test_pms_custom_field import PMSCustomFieldTestFixture, PMSCustomField
from pms_app.properties.models.property.test_property import PropertyFixtures, Property


class PMSCustomFieldValueFixtures(RenovationTestFixture):

    def __init__(self):
        super().__init__()
        self.DEFAULT_MODEL = PMSCustomFieldValue
        self.dependent_fixtures = [PMSCustomFieldTestFixture]

    async def make_fixtures(self):
        for cf in self.get_dependencies(PMSCustomField):
            for entity_type in cf.get_applicable_entity_types():
                for entity in renovation.local.db.get_all(entity_type):
                    self.add_document(await PMSCustomFieldValue(dict(
                        entity_type=entity_type,
                        entity=entity.name,
                        fieldname=cf.fieldname,
                        value=self.get_random_value(cf)
                    )).insert())

    def get_random_value(self, cf: PMSCustomField):
        f = Faker()
        value = f.first_name()

        if cf.fieldtype == "Float":
            value = f.random_int() + 100 / 1000
        elif cf.fieldtype == "Integer":
            value = f.random_int()
        elif cf.fieldtype == "Select":
            value = f.random.choice(cf.options.split("\n"))

        return value


class TestPMSCustomFieldValue(TestCase):

    properties = PropertyFixtures()
    custom_field_values = PMSCustomFieldValueFixtures()
    faker = Faker()

    @classmethod
    @runnify
    async def setUpClass(cls):
        await cls.properties.setUp()
        await cls.custom_field_values.setUp()

    @classmethod
    @runnify
    async def tearDownClass(cls):
        await cls.custom_field_values.tearDown()
        await cls.properties.tearDown()

    async def _get_random_custom_field_value_doc(self):
        return PMSCustomFieldValue(dict(
            fieldname=self.faker.first_name(),
            entity_type=Property.get_doctype(),
            entity=await Property.db_get_value(dict()),
            value=self.faker.last_name(),
        ))

    @runnify
    async def test_random_fieldname(self):
        d = await self._get_random_custom_field_value_doc()

        with self.assertRaises(NotFound):
            await d.insert()

    @runnify
    async def test_random_entity_type(self):
        d = await self._get_random_custom_field_value_doc()
        cf_data = await PMSCustomField.db_get_value(dict(fieldtype="Data"), "fieldname")

        d.fieldname = cf_data
        d.entity_type = "User"
        d.entity = "Administrator"
        d.value = "A"

        with self.assertRaises(CustomFieldNotApplicableOnEntityType):
            await d.save()

    @runnify
    async def test_data_field(self):
        d = await self._get_random_custom_field_value_doc()
        cf_data = await PMSCustomField.db_get_value(dict(fieldtype="Data"), "fieldname")

        d.fieldname = cf_data
        d.entity_type = Property.get_doctype()
        d.entity = self.properties[0].name
        d.value = 23

        await d.save()
        await d.reload()
        self.custom_field_values.add_document(d)
        self.assertEqual(d.value, "23")

        d.value = "Hey!"
        await d.save()
        await d.reload()
        self.assertEqual(d.value, "Hey!")

    @runnify
    async def test_float_field(self):
        d = await self._get_random_custom_field_value_doc()
        cf_float = await PMSCustomField.db_get_value(dict(fieldtype="Float"), "name")
        cf_float = await PMSCustomField.get_doc(cf_float)

        d.fieldname = cf_float.fieldname
        d.entity_type = cf_float.get_applicable_entity_types()[0]
        d.entity = renovation.local.db.get_value(cf_float.get_applicable_entity_types()[0], dict())
        d.value = 2.5

        await d.save()
        await d.reload()
        self.custom_field_values.add_document(d)
        self.assertEqual(d.value, "2.5")

    @runnify
    async def test_integer_field(self):
        d = await self._get_random_custom_field_value_doc()
        cf_int = await PMSCustomField.db_get_value(dict(fieldtype="Integer"), "name")
        cf_int = await PMSCustomField.get_doc(cf_int)

        d.fieldname = cf_int.fieldname
        d.entity_type = cf_int.get_applicable_entity_types()[0]
        d.entity = renovation.local.db.get_value(cf_int.get_applicable_entity_types()[0], dict())
        d.value = 3

        await d.save()
        await d.reload()
        self.custom_field_values.add_document(d)
        self.assertEqual(d.value, "3")

    @runnify
    async def test_select_field(self):
        d = await self._get_random_custom_field_value_doc()
        cf_select = await PMSCustomField.db_get_value(dict(fieldtype="Select"), "name")
        cf_select = await PMSCustomField.get_doc(cf_select)

        options = cf_select.options.split("\n")

        d.fieldname = cf_select.fieldname
        d.entity_type = cf_select.get_applicable_entity_types()[0]
        d.entity = renovation.local.db.get_value(cf_select.get_applicable_entity_types()[0], dict())
        d.value = options[0]

        await d.save()
        await d.reload()
        self.custom_field_values.add_document(d)
        self.assertEqual(d.value, options[0])

        d.value = "RANDOM OPTION"
        with self.assertRaises(InvalidValueForSelectField):
            await d.save()

    @runnify
    async def test_delete_cf(self):
        cf = PMSCustomField(dict(
            label="Test ABCDEF",
            fieldtype="Data",
        ))
        await cf.insert()

        for dt in cf.get_applicable_entity_types():
            for dn in renovation.local.db.get_all(dt):
                self.custom_field_values.add_document(await PMSCustomFieldValue(dict(
                    fieldname=cf.fieldname,
                    entity_type=dt, entity=dn.name,
                    value=self.faker.first_name()
                )).insert())

        # Lets delete
        await cf.delete()

        # Make sure there exists CFValues that belonged to the fieldname we just deleted
        values = await PMSCustomFieldValue.get_all(dict(fieldname=cf.fieldname))
        self.assertGreater(len(values), 0)
