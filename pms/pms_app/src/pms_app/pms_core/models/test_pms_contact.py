import unittest

import renovation
from renovation.tests import RenovationTestFixture
from .pms_contact import PMSContact


class PMSContactFixtures(RenovationTestFixture):

    def __init__(self):
        super().__init__()
        self.DEFAULT_MODEL = PMSContact

    async def make_fixtures(self):

        fixture1 = PMSContact(renovation._dict(
            first_name="Test beneficiary 1"
        ))
        await fixture1.insert()
        self.add_document(fixture1)


class TestPMSContact(unittest.TestCase):
    pass
