import json
import requests
from helpers.config import config
from helpers.logger import Logger

logger = Logger().getLogger()

class APIv2:
    """
    Provides direct access to api.combahton.net/v2
    """

    headers = {
        "User-Agent": "combahton_cli/{}".format(__module__)
    }

    def __init__(self):
        self.scope = "https://api.combahton.net/v2"
        self.auth_user = config.get("CB_AUTH_USER")
        self.auth_secret = config.get("CB_AUTH_SECRET")

    def request(self, **kwargs):
        """Send a request to api.combahton.net/v2 using kwargs"""
        post_data = {
            "email": self.auth_user,
            "secret": self.auth_secret
        }

        for key, value in kwargs.items():
            post_data[key] = value

        logger.debug("Sending request to {scope:s} with params: {param:s}".format(scope = self.scope, param = json.dumps(post_data)))

        request = requests.post(self.scope, json=post_data, headers=self.headers)