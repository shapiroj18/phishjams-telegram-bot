import os
import sys

topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)

from phish_bot.phishnet_api import PhishNetAPI

phishnet_api = PhishNetAPI()


def test_get_root_endpoint():
    """Tests basic functionality of phish.net v3 endpoint"""
    response = phishnet_api.get_root_endpoint()
    assert response.status_code == 200
