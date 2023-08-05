from pytest_bdd import scenario, given, when, then, parsers
import re
import os
import pytest
from click.testing import CliRunner
from paylense.collections import Collections


pytest.globalDict = {}


@scenario('features/collections.feature', 'Request a payment from a consumer (Payer)')
def test_collections():
    pass


@given("I have a valid APP-ID, username and password")
def user_credentials():
    config = {
        "PAYLENSE_APP_ID": os.environ.get("PAYLENSE_APP_ID"),
        "PAYLENSE_USERNAME": os.environ.get("PAYLENSE_USERNAME"),
        "PAYLENSE_PASSWORD": os.environ.get("PAYLENSE_PASSWORD"),
    }
    client = Collections(config)
    pytest.globalDict["client"] = client


@when("I request for a payment with the following payment details\n| note         | amount | message | mobile     | product_id |\n| test payment | 600    | message | 0782631873 |")
def successful_request_to_pay():

    ref = pytest.globalDict["client"].requestToPay(
        mobile="256772123456", amount="600", processing_number="123456789", narrartion="narr")
    pytest.globalDict["ref"] = ref


@when("I check for transaction Status")
def check_transaction_status():
    status = pytest.globalDict["client"].getTransactionStatus(pytest.globalDict["ref"]["processing_number"])
    pytest.globalDict["status"] = status
    assert isinstance(status, dict)
    assert "amount" in status.keys()


@then("It should be successful")
def successful_transaction():
    assert pytest.globalDict["status"]["status"] == "SUCCESSFUL"
