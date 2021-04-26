import requests
from helpers.logger import Logger

logger = Logger().get_logger()

class External:  # pylint: disable=too-few-public-methods
    """Provides access to external resources of other providers to eg. resolve the external IPv4 of the client"""
    @staticmethod
    def resolve_external_ipv4():
        response = requests.get("https://ifconfig.me/ip")
        return response.text
