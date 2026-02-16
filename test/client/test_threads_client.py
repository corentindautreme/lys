import unittest
import datetime
import requests
import os
import json

from unittest.mock import patch, Mock
from requests.exceptions import HTTPError

from utils.settings_utils import SettingsUtils
from client.threads_client import ThreadsClient
from client.publish_error import PublishError

class ThreadsClientTest(unittest.TestCase):
    PUBLISH_ERROR_BODY = """{
        "error": {
            "message": "The requested resource does not exist",
            "type": "OAuthException",
            "code": 24,
            "error_subcode": 4279009,
            "is_transient": False,
            "error_user_title": "Contenu multimédia introuvable",
            "error_user_msg": "Le contenu multimédia présentant l'ID 1 est introuvable.",
            "fbtrace_id": "AA0_abcdeFgHIJ12kl_mn3O"
        }
    }"""
    PUBLISH_ERROR_RESPONSE = requests.Response()
    PUBLISH_ERROR_RESPONSE.status_code=404
    PUBLISH_ERROR_RESPONSE._content=PUBLISH_ERROR_BODY.encode('utf-8')


    def raise_exception(self, e):
        raise e


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with patch.dict(os.environ, {"THREADS_USER_ID": "MOCK_USER_ID", "THREADS_ACCESS_TOKEN": "MOCK_TOKEN"}):
            self.client = ThreadsClient(retry_delays=[0, 1, 1, 1, 1, 1])
            self.client.create_session()


    def test_when_publishing_post_to_threads_fails_should_retry(self):
        responses = [
            Mock(status_code=202, json=lambda: {'id': '1'}, raise_for_status=lambda: True),
            Mock(status_code=404, raise_for_status=lambda: self.raise_exception(HTTPError("", 404, response=self.PUBLISH_ERROR_RESPONSE)), json=lambda: self.PUBLISH_ERROR_BODY),
            Mock(status_code=202, json=lambda: {'id': '1'}, raise_for_status=lambda: True)
        ]
        with patch.object(requests, 'post', side_effect=responses):
            (new_post_id, root_post_id) = self.client.publish(post="This is a post")
            self.assertEqual(new_post_id, '1')
            self.assertEqual(root_post_id, '1')


    def test_when_publishing_post_to_threads_fails_for_all_attemps_should_throw_exception(self):
        responses = [
            Mock(status_code=202, json=lambda: {'id': '1'}, raise_for_status=lambda: True),
            Mock(status_code=404, raise_for_status=lambda: self.raise_exception(HTTPError("", 404, response=self.PUBLISH_ERROR_RESPONSE)), json=lambda: self.PUBLISH_ERROR_BODY),
            Mock(status_code=404, raise_for_status=lambda: self.raise_exception(HTTPError("", 404, response=self.PUBLISH_ERROR_RESPONSE)), json=lambda: self.PUBLISH_ERROR_BODY),
            Mock(status_code=404, raise_for_status=lambda: self.raise_exception(HTTPError("", 404, response=self.PUBLISH_ERROR_RESPONSE)), json=lambda: self.PUBLISH_ERROR_BODY),
            Mock(status_code=404, raise_for_status=lambda: self.raise_exception(HTTPError("", 404, response=self.PUBLISH_ERROR_RESPONSE)), json=lambda: self.PUBLISH_ERROR_BODY),
            Mock(status_code=404, raise_for_status=lambda: self.raise_exception(HTTPError("", 404, response=self.PUBLISH_ERROR_RESPONSE)), json=lambda: self.PUBLISH_ERROR_BODY)
        ]
        with patch.object(requests, 'post', side_effect=responses) as mock_req:
            with self.assertRaises(PublishError) as context:
                self.client.publish(post="This is a post")
            self.assertEqual(str(context.exception), "Unable to publish created post to Thread - status is 404")
