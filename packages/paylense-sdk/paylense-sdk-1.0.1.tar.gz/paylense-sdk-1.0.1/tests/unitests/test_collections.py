import unittest
import pytest
import types
try:
    from unittest import mock
except ImportError:
    import mock

from requests import Request, Session

from .utils import mocked_requests_get, mocked_requests_post, mocked_requests_session
from paylense.errors import ValidationError
from paylense.client import Paylense
from paylense.collections import Collections


class TestCollections(unittest.TestCase):

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def setUp(self, mock_get):
        self.config = {
            "PAYLENSE_APP_ID": "110000",
            "PAYLENSE_USERNAME": "sdk",
            "PAYLENSE_PASSWORD": "sdk@2020"
        }
        client = Collections(self.config)
        self.client = client

    def tearDown(self):
        pass

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_client_instantiate(self, mock_get):

        client = Collections(self.config)

        assert isinstance(client, Collections)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_invalid_uuid(self, mock_get):
        with self.assertRaises(ValidationError):
            config = self.config
            client = Collections(config)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_invalid_mobile(self, mock_get):
        with self.assertRaises(ValidationError):
            ref = self.client.requestToPay(mobile="256712123456", amount="600",
                                           processing_number="123456789", narration="dd")
        with self.assertRaises(ValidationError):
            ref = self.client.requestToPay(mobile="254712123456", amount="600",
                                           processing_number="123456789", narration="dd")

    @mock.patch.object(Paylense, "request", side_effect=mocked_requests_session)
    def test_request_to_pay(self, mock_get):

        ref = self.client.requestToPay(mobile="256772123456", amount="600", processing_number="123456789", narration="dd")

        assert isinstance(ref, dict)
        assert "processing_number" in ref.keys()

    @mock.patch.object(Paylense, "request", side_effect=mocked_requests_session)
    def test_get_transaction_status(self, mock_get):
        status = self.client.getTransactionStatus("dummy")
        assert isinstance(status, dict)
        assert "amount" in status.keys()
