import ipaddress

import click
from tabulate import tabulate

from helpers.config import config # pylint: disable=import-error,no-name-in-module
from helpers.api import APIv2 # pylint: disable=import-error,no-name-in-module
from helpers.logger import Logger # pylint: disable=import-error,no-name-in-module

api = APIv2()
log = Logger().get_logger()

@click.group()
def ipaddr():
    """Provides access to ip address details from combahton.net"""

@click.command(name="get-rdns")
@click.argument("address", default=config.get("CB_DEFAULT_IP"))
@click.option("-f", "--format", "output_format", type=click.Choice(['table','json'], case_sensitive=False), default='table')
def ipaddr_get_rdns(address,output_format):
    """View details about the specified ip address. If you do not specify an IP address, CB_DEFAULT_IP will be used."""
    action = "none"
    try:
        address = ipaddress.ip_address(address)
        if isinstance(address, ipaddress.IPv4Address):
            action = "ipv4"
        elif isinstance(address, ipaddress.IPv6Address):
            action = "ipv6"

        response = api.request(component = "ipaddr", method="view", action=action, ipaddr = str(address))
        if "status" in response:
            res_status = api.parse_status(response["status"])
            if res_status:
                log.log(res_status["level"], res_status["message"])
        else:
            if output_format == "table":
                click.echo(tabulate(([k, v] for k, v in response.items())))
            elif output_format == "json":
                click.echo(response)
    except (ValueError, ipaddress.AddressValueError) as error:
        log.error(error)

ipaddr.add_command(ipaddr_get_rdns)

@click.command(name="set-rdns")
@click.argument("rdns", type=click.STRING)
@click.argument("address", default=config.get("CB_DEFAULT_IP"))
def ipaddr_set_rdns(rdns, address):
    """Set RNDS for the specified ip address. If you do not specify an IP address, CB_DEFAULT_IP will be used."""
    action = "none"
    try:
        address = ipaddress.ip_address(address)
        if isinstance(address, ipaddress.IPv4Address):
            action = "ipv4"
        elif isinstance(address, ipaddress.IPv6Address):
            action = "ipv6"

        response = api.request(component = "ipaddr", method="rdns", action=action, ipaddr = str(address), ptr = rdns)
        if "status" in response:
            res_status = api.parse_status(response["status"])
            if res_status:
                log.log(res_status["level"], res_status["message"])
    except (ValueError, ipaddress.AddressValueError) as error:
        log.error(error)

ipaddr.add_command(ipaddr_set_rdns)

@click.command(name="set-nexthop")
@click.argument("contract", type=click.INT)
@click.argument("address", default=config.get("CB_DEFAULT_IP"))
def ipaddr_set_nexthop(contract, address):
    """Set RNDS for the specified ip address. If you do not specify an IP address, CB_DEFAULT_IP will be used."""
    try:
        address = ipaddress.ip_address(address)
        if not isinstance(address, ipaddress.IPv4Address):
            raise ValueError()
        response = api.request(component = "ipsubnet", method="nexthop", action="change", contract = contract, nexthop = str(address))
        if "status" in response:
            res_status = api.parse_status(response["status"])
            if res_status:
                log.log(res_status["level"], res_status["message"])
    except (ValueError, ipaddress.AddressValueError) as error:
        log.error(error)

ipaddr.add_command(ipaddr_set_nexthop)
