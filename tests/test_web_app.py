import json
import os
import random
import string

from commonlib.tests.common.athena_test_utils import AthenaTestMixin
from mock import patch, MagicMock, call, Mock
from unittest2 import TestCase
from zeus.utils.testutils import AppTestMixin

from data_api import data_api
from views import chat_api
from webapp_chatbot import app


class TestChatApp(AppTestMixin, AthenaTestMixin, TestCase):
    __URL_PREFIX__ = 'chat_bot'
    __TEST_APP__ = app
    __CUSTOMER_NAME__ = 'chat_bot_customer'

    def setUp(self):
        os.environ['ATHENA_CSRF_DISABLE'] = 'true'
        super(TestChatApp, self).setUp()
        self.base_api = self.__URL_PREFIX__

    def set_session(self, user=None):
        with self.app as c:
            with c.session_transaction() as sess:
                sess['user_id'] = user or self.__TEST_USER_EMAIL__
                sess['_fresh'] = True

    def test_chat(self):
        self.set_session()
        with self.app as c:
            url = '{}/chat'.format(self.base_api)
            rv = c.post(url, headers={'Cookie': self.__SESSION_COOKIES__}, data="highlights")
            self.assertEqual(rv.status_code, 200)
            self.assertIsNotNone(rv.data)
