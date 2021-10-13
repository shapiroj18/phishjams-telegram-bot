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


def test_post_subscribe_mjm(heroku_flask_url):
    test_chat_id = 1
    resp = api_requests.post_subscribe_mjm(heroku_flask_url, test_chat_id)
    assert resp == "1 has been subscribed successfully!"


def test_post_subscribe_mjm_error(heroku_flask_url):
    with pytest.raises(json.decoder.JSONDecodeError):
        test_chat_id = "test_chat_id"
        api_requests.post_subscribe_mjm(heroku_flask_url, test_chat_id)


def test_post_unsubscribe_mjm(heroku_flask_url):
    test_chat_id = 1
    resp = api_requests.post_subscribe_mjm(heroku_flask_url, test_chat_id)
    assert resp == "1 removed successfully!"


def test_post_unsubscribe_mjm(heroku_flask_url):
    test_chat_id = 123
    resp = api_requests.post_subscribe_mjm(heroku_flask_url, test_chat_id)
    assert resp == "123 did not exist in the database"


def test_post_unsubscribe_mjm(heroku_flask_url):
    test_chat_id = 123320840293842
    with pytest.raises(json.decoder.JSONDecodeError):
        resp = api_requests.post_subscribe_mjm(heroku_flask_url, test_chat_id)
