import json
import requests
from helpers.config import config
from helpers.logger import Logger

logger = Logger().get_logger()

class APIv2:
    """
    Provides direct access to api.combahton.net/v2
    """
    status_list = {
        # General messages
        "error":  { "level": logger.FATAL, "message": "An unknown error occured." },
        "auth_params_undefined": { "level": logger.FATAL, "message": "You have not provided any user details." },
        "id_unauthenticated": { "level": logger.ERROR, "message": "The specified user does not have access to the given object." },
        "layer7_challenge": { "level": logger.FATAL, "message": """
                                          ..-^~~~^-..
                                        .~           ~.
                                       (;:           :;)
                                        (:           :)
                                          ':._   _.:'
                                              | |
                                            (=====)
                                              | |
        -O-                                   | |
          \\                                   | |
          /\\                               ((/   \\))
        Houston, We Have A Problem. API responds with Layer7 challenge.
        This should never happen. Please contact our customer support."""},
        # AntiDDoS Module
        "ssl_chain_invalid": { "level": logger.ERROR, "message": "The specified SSL chain was invalid. Please check your input." },
        "exists": { "level": logger.ERROR, "message": "The specified domain already exists on the Layer 7 filters." },
        "added": { "level": logger.INFO, "message": "The domain/certificate was successfully added to the Layer 7 filters." },
        "deleted": { "level": logger.INFO, "message": "The domain/certificate was successfully removed from the layer 7 filters." },
        "routing_changed": { "level": logger.INFO, "message": "The routing was successfully changed." },
        # Cloud Module
        "id_reinstalling": { "level": logger.ERROR, "message": "The specified cloud server is currently being reinstalled." },
        "OK": { "level": logger.INFO, "message": "The task has been executed successfully." },
        # Customer/Contract Module
        "invoices_paid": { "level": logger.INFO, "message": "The specified user has no unpaid invoices."},
        "extended":  { "level": logger.INFO, "message": "The specified contract was successfully extended."},
        "autoextend_disabled":  { "level": logger.INFO, "message": "Successfully disabled automatic renewal for the specified contract."},
        "autoextend_enabled":  { "level": logger.INFO, "message": "Successfully activated automatic renewal for the specified contract."},
        "order_placed":  { "level": logger.INFO, "message": "The order was successfully processed."},
        # IPAddr Module
        "rdns_changed":  { "level": logger.INFO, "message": "The RDNS/PTR was successfully set for the specified address."},
        "success": { "level": logger.INFO, "message": "The task has been executed successfully." },
    }

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
        response = requests.post(self.scope, json=post_data, headers=self.headers, cookies={ 'layer7-validate': '83a4bb9f6e41b49cb63645bca5600b10'})
        if "Authentication required" in response.text:
            return { "status": "layer7_challenge" }

        if response.headers["Content-Type"] == "application/pdf":
            return response

        logger.debug(response.text)
        try:
            logger.debug("Parsing response as JSON")
            return json.loads(response.text)
        except (json.JSONDecodeError, ValueError):
            try:
                logger.debug("Trying to fix malformed json")
                json_fix = self.try_fix_json(response.text)
                if json_fix:
                    logger.debug("JSON has been fixed.")
                    return json_fix
                else:
                    logger.debug("JSON could not be parsed. Falling back to plain text")
                    return response.text
            except ValueError:
                logger.debug("JSON could not be parsed. Falling back to plain text")
                return response.text

    def parse_status(self, status, *args):
        if status in self.status_list:
            result = self.status_list.get(status, lambda: { "level": logger.FATAL, "message": "An unknown error occured." })
            if len(args) > 0:
                result["message"] = "{} ({})".format(result["message"], json.dumps(args))
            return result
        else:
            return False

    @staticmethod
    def try_fix_json(badjson):
        goodjson = badjson.replace("}{", "},{")
        try:
            return json.loads(goodjson)
        except (json.JSONDecodeError, ValueError):
            return False
