import os
import json
import httpx
import pytest
from dotenv import load_dotenv
from commands.lib.api_requests import APIRequests

api_requests = APIRequests()
load_dotenv()


def test_post_subscribe_daily_jams_success():
    heroku_flask_url = os.getenv("HEROKU_FLASK_URL")
    test_email = "iamatestemail@gmail.com"
    test_chat_id = "test_chat_id"
    response = api_requests.post_subscribe_daily_jams(
        heroku_flask_url, test_email, test_chat_id
    )
    assert response == f"{test_email} subscribed successfully"
    
def test_post_subscribe_daily_jams_error_jsondecodeerror():
    with pytest.raises(json.decoder.JSONDecodeError):
        heroku_flask_url = os.getenv("HEROKU_FLASK_URL")
        test_email = ""
        test_chat_id = "test_chat_id"
        response = api_requests.post_subscribe_daily_jams(
            heroku_flask_url, test_email, test_chat_id
        )


def test_post_subscribe_daily_jams_error_unsupportedprotocol():
    with pytest.raises(httpx.UnsupportedProtocol):
        
        heroku_flask_url = ''
        test_email = "iamatestemail@gmail.com"
        test_chat_id = "test_chat_id"
        response = api_requests.post_subscribe_daily_jams(
            heroku_flask_url, test_email, test_chat_id
        )