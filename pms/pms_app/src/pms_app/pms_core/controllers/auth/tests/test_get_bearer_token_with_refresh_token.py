from unittest import TestCase
from asyncer import runnify

import renovation
from renovation.utils.auth import update_user_password
from ..get_bearer_token_with_refresh_token import get_bearer_token_with_refresh_token
from ..get_bearer_token_with_password import get_bearer_token_with_password
from pms_app.pms_core.models.pms_contact.test_pms_contact import PMSContactFixtures


class TestTokenRefresh(TestCase):

    pms_contacts = PMSContactFixtures(make_users=True)

    @classmethod
    @runnify
    async def setUpClass(cls):
        await cls.pms_contacts.setUp()

    @classmethod
    @runnify
    async def tearDownClass(cls):
        if renovation.user != "Administrator":
            renovation.set_user("Administrator")
        await cls.pms_contacts.tearDown()

    @runnify
    async def test_simple(self):
        # TODO: mock renovation.local.request to test this
        # pms_contact = self.pms_contacts[0]
        # new_pwd = "myHardPassword12"
        # await update_user_password(pms_contact.user, new_pwd)

        # r = await get_bearer_token_with_password(pms_contact.user, new_pwd)
        # self.assertEqual(renovation.user, pms_contact.user)

        # for k in ("pms_contact_info", "access_token", "refresh_token"):
        #     self.assertIsNotNone(r.get(k))

        # r1 = await get_bearer_token_with_refresh_token(refresh_token=r.refresh_token)
        # print(r1)
        pass
