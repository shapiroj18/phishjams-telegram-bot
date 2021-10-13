import os
import json
import httpx
import pytest
from dotenv import load_dotenv
from commands.lib.api_requests import APIRequests

api_requests = APIRequests()
load_dotenv()


@pytest.fixture
def heroku_flask_url():
    return os.getenv("HEROKU_FLASK_URL")


def test_post_subscribe_daily_jams_success(heroku_flask_url):
    test_email = "iamatestemail@gmail.com"
    test_chat_id = "test_chat_id"
    response = api_requests.post_subscribe_daily_jams(
        heroku_flask_url, test_email, test_chat_id
    )
    assert response == f"{test_email} subscribed successfully"


def test_post_subscribe_daily_jams_error_jsondecodeerror(heroku_flask_url):
    with pytest.raises(json.decoder.JSONDecodeError):
        test_email = ""
        test_chat_id = "test_chat_id"
        response = api_requests.post_subscribe_daily_jams(
            heroku_flask_url, test_email, test_chat_id
        )


def test_post_subscribe_daily_jams_error_unsupportedprotocol():
    with pytest.raises(httpx.UnsupportedProtocol):

        heroku_flask_url = ""
        test_email = "iamatestemail@gmail.com"
        test_chat_id = "test_chat_id"
        response = api_requests.post_subscribe_daily_jams(
            heroku_flask_url, test_email, test_chat_id
        )


def test_post_unsubscribe_daily_jams_success(heroku_flask_url):
    test_email = "iamatestemail@gmail.com"
    response = api_requests.post_unsubscribe_daily_jams(heroku_flask_url, test_email)
    assert response == f"{test_email} removed successfully"


def test_post_unsubscribe_daily_jams_success(heroku_flask_url):
    test_email = "emailnotindatabse@gmail.com"
    response = api_requests.post_unsubscribe_daily_jams(heroku_flask_url, test_email)
    assert response == f"{test_email} did not exist in the database"


def test_post_unsubscribe_daily_jams_error_unsupportedprotocol():
    with pytest.raises(httpx.UnsupportedProtocol):
        heroku_flask_url = ""
        test_email = "iamatestemail@gmail.com"
        response = api_requests.post_unsubscribe_daily_jams(
            heroku_flask_url, test_email
        )
