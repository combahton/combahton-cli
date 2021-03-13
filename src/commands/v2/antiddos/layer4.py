import ipaddress
import click
from helpers.api import APIv2 # pylint: disable=import-error,no-name-in-module
from helpers.logger import Logger # pylint: disable=import-error,no-name-in-module
from helpers.config import config # pylint: disable=import-error,no-name-in-module

api = APIv2()
log = Logger().get_logger()

@click.group()
def layer4():
    """Methods to access and modify the layer 4 filter settings"""

@click.command(name="set-routing")
@click.argument("routing_type", type=click.Choice(['dynamic','permanent','dynamic_perm']))
@click.argument("ipv4", default=config.get("CB_DEFAULT_IP"))
def l4_routing(routing_type, ipv4):
    """Set the Layer 4 routing mode of the specified IPv4
    Valid routing types are dynamic, permanent, dynamic_perm"""
    try:
        ipaddr = str(ipaddress.ip_address(ipv4))
        response = api.request(component = "antiddos", method = "layer4", action = "routing", routing = routing_type, ipaddr = ipaddr)
        if "status" in response:
            res_status = api.parse_status(response["status"])
            log.log(res_status["level"], res_status["message"])
        else:
            log.fatal("An unknown error occured.")
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError, ValueError) as error:
        log.error(error)

layer4.add_command(l4_routing)
