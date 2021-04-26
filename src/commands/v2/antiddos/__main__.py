import ipaddress
import click
from tabulate import tabulate # pylint: disable=import-error
from helpers.api import APIv2 # pylint: disable=import-error,no-name-in-module
from helpers.logger import Logger # pylint: disable=import-error,no-name-in-module
from helpers.config import config # pylint: disable=import-error,no-name-in-module

from commands.v2.antiddos.layer4 import layer4 # pylint: disable=import-error,no-name-in-module
from commands.v2.antiddos.layer7 import layer7 # pylint: disable=import-error,no-name-in-module
from commands.v2.antiddos.incidents import incidents # pylint: disable=import-error,no-name-in-module

api = APIv2()
log = Logger().get_logger()

@click.group()
def antiddos():
    """Provides access to AntiDDoS Options of combahton.net"""

@click.command()
@click.argument("ipv4", default=config.get("CB_DEFAULT_IP"))
@click.option("-f", "--format", "output_format", type=click.Choice(['table','json'], case_sensitive=False), default='table')
def status(ipv4, output_format):
    """Shows the filter status of the specified IPv4 address"""
    try:
        ipaddr = str(ipaddress.ip_address(ipv4))
        response = api.request(component = "antiddos", method = "status", action = "show", ipaddr = ipaddr)
        if "status" in response:
            res_status = api.parse_status(response["status"])
            log.log(res_status["level"], res_status["message"])
        else:
            if output_format == "table":
                click.echo(tabulate([k, v] for k, v in response.items()))
            elif output_format == "json":
                click.echo(response)

    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError) as error:
        log.error("address/netmask is invalid: %s", error)
        raise
    except:
        log.error("Usage: antiddos status IPv4Address")
        raise

antiddos.add_command(status)
antiddos.add_command(layer4)
antiddos.add_command(layer7)
antiddos.add_command(incidents)
