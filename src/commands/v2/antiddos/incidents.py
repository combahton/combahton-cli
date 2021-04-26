import ipaddress
from datetime import datetime
from tabulate import tabulate # pylint: disable=import-error
import click
from helpers.api import APIv2 # pylint: disable=import-error,no-name-in-module
from helpers.logger import Logger # pylint: disable=import-error,no-name-in-module
from helpers.config import config # pylint: disable=import-error,no-name-in-module

api = APIv2()
log = Logger().get_logger()

@click.group()
def incidents():
    """Shows previous incidents of the AntiDDoS infrastructure"""

@click.command(name="single")
@click.argument("ipv4", default=config.get("CB_DEFAULT_IP"))
@click.option("-f", "--format", "output_format", type=click.Choice(['table','json'], case_sensitive=False), default='table')
@click.option("-H", "--human-readable", "human", is_flag=True, default=False)
def incidents_single(ipv4, output_format, human):
    """Shows the last 25 ddos incidents for the specified IP address."""
    try:
        ipaddr = str(ipaddress.ip_address(ipv4))
        response = api.request(component = "antiddos", method = "incidents", action = "show", ipaddr = ipaddr)
        if "status" in response:
            res_status = api.parse_status(response["status"])
            log.log(res_status["level"], res_status["message"])
        else:
            if human:
                for k, val in enumerate(response):
                    response[k]["time"] = datetime.utcfromtimestamp(int(val["time"])).strftime('%Y-%m-%d %H:%M:%S UTC')

            if output_format == "table":
                click.echo(tabulate(response, headers="keys"))
            else:
                click.echo(response)
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError, ValueError) as error:
        log.error(error)

incidents.add_command(incidents_single)

@click.command(name="all")
@click.option("-f", "--format", "output_format", type=click.Choice(['table','json'], case_sensitive=False), default='table')
@click.option("-H", "--human-readable", "human", is_flag=True, default=False)
def incidents_all(output_format, human):
    """Shows the last 100 ddos incidents for all IP addresses the provided user has access to."""
    try:
        response = api.request(component = "antiddos", method = "incidents", action = "show_all")
        if "status" in response:
            res_status = api.parse_status(response["status"])
            log.log(res_status["level"], res_status["message"])
        else:
            if human:
                for k, val in enumerate(response):
                    response[k]["time"] = datetime.utcfromtimestamp(int(val["time"])).strftime('%Y-%m-%d %H:%M:%S UTC')

            if output_format == "table":
                click.echo(tabulate(response, headers="keys"))
            else:
                click.echo(response)
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError, ValueError) as error:
        log.error(error)

incidents.add_command(incidents_all)
