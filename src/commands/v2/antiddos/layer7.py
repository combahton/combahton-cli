import ipaddress
import click
from tabulate import tabulate # pylint: disable=import-error
from helpers.api import APIv2 # pylint: disable=import-error,no-name-in-module
from helpers.logger import Logger # pylint: disable=import-error,no-name-in-module
from helpers.config import config # pylint: disable=import-error,no-name-in-module

api = APIv2()
log = Logger().get_logger()

@click.group()
def layer7():
    """Methods to access and modify the layer 7 filter settings"""

@click.command(name="set-routing")
@click.argument("routing_type", type=click.Choice(['only_on','only_off','activate','deactivate']))
@click.argument("ipv4", default=config.get("CB_DEFAULT_IP"))
def l7_routing(routing_type, ipv4):
    """Set the Layer 7 routing mode of the specified IPv4
    Valid routing types are only_on, only_off, activate, deactivate"""
    try:
        ipaddr = str(ipaddress.ip_address(ipv4))
        response = api.request(component = "antiddos", method = "layer7", action = "routing", routing = routing_type, ipaddr = ipaddr)
        if "status" in response:
            res_status = api.parse_status(response["status"])
            log.log(res_status["level"], res_status["message"])
        else:
            log.fatal("An unknown error occured.")
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError, ValueError) as error:
        log.error(error)

layer7.add_command(l7_routing)

@click.command(name="domain-add")
@click.argument("domain")
@click.argument("protector", type=click.Choice(['aes','button','captcha']), default='button')
def l7_domain_add(domain, protector):
    """Adds a DOMAIN to the layer 7 filtering infrastructure, optionally setting the PROTECTOR
    DOMAIN is a FQDN, whose A-Record points to an IPv4 address owned by your account.
    PROTECTOR is one of aes, button, captcha - defaults to button.
    """
    try:
        response = api.request(component = "antiddos", method = "layer7", action = "add", domain = domain, protector = protector)
        if "status" in response:
            res_status = api.parse_status(response["status"])
            log.log(res_status["level"], res_status["message"])
        else:
            log.fatal("An unknown error occured.")
    except ValueError as error:
        log.error(error)

layer7.add_command(l7_domain_add)

@click.command(name="domain-remove")
@click.argument("domain")
def l7_domain_remove(domain):
    """Removes a DOMAIN from the layer 7 filtering infrastructure.
    """
    try:
        response = api.request(component = "antiddos", method = "layer7", action = "delete", domain = domain)
        if "status" in response:
            res_status = api.parse_status(response["status"])
            log.log(res_status["level"], res_status["message"])
        else:
            log.fatal("An unknown error occured.")
    except ValueError as error:
        log.error(error)

layer7.add_command(l7_domain_remove)

@click.command(name="ssl-add")
@click.argument("domain")
@click.argument("certificate", type=click.File("r"))
@click.argument("private-key", type=click.File("r"))
@click.argument("protector", type=click.Choice(['aes','button','captcha']), default='button')
def l7_ssl_add(domain, certificate, private_key, protector):
    """Adds an SSL secured DOMAIN to the layer 7 filtering infrastructure, optionally setting the PROTECTOR.
    Requires the path to CERTIFICATE and PRIVATE-KEY. PROTECTOR is one of aes, button, captcha - defaults to button."""
    try:
        response = api.request(component = 'antiddos', method = 'layer7', action = 'ssl_add', domain = domain, cert = certificate.read(), key = private_key.read(), protector = protector)
        if "status" in response:
            res_status = api.parse_status(response["status"])
            log.log(res_status["level"], res_status["message"])
        else:
            click.echo(response)
    except ValueError as err:
        log.error(err)

layer7.add_command(l7_ssl_add)

@click.command(name="ssl-remove")
@click.argument("domain")
def l7_ssl_remove(domain):
    """Removes an SSL secured DOMAIN from the layer 7 filtering infrastructure."""
    try:
        response = api.request(component = 'antiddos', method = 'layer7', action = 'ssl_delete', domain = domain)
        if "status" in response:
            res_status = api.parse_status(response["status"])
            log.log(res_status["level"], res_status["message"])
        else:
            click.echo(response)
    except ValueError as err:
        log.error(err)

layer7.add_command(l7_ssl_remove)

@click.command(name="ssl-view")
@click.option("-f", "--format", "output_format", type=click.Choice(['table','json'], case_sensitive=False), default='table')
def l7_ssl_view(output_format):
    """Shows all SSL secured DOMAINs on the layer 7 filtering infrastructure."""
    try:
        response = api.request(component = 'antiddos', method = 'layer7', action = 'ssl_view')
        if "status" in response:
            res_status = api.parse_status(response["status"])
            log.log(res_status["level"], res_status["message"])
        else:
            if output_format == "table":
                click.echo(tabulate(([v["domain"]] for v in response), headers=["Domains"]))
            elif output_format == "json":
                click.echo(response)
    except ValueError as err:
        log.error(err)

layer7.add_command(l7_ssl_view)
