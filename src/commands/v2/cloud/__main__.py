import click
from tabulate import tabulate

from commands.v2.cloud.reinstall import reinstall # pylint: disable=import-error,no-name-in-module

from helpers.api import APIv2 # pylint: disable=import-error,no-name-in-module
from helpers.logger import Logger # pylint: disable=import-error,no-name-in-module
from helpers.external import External  # pylint: disable=import-error,no-name-in-module

ext = External()
api = APIv2()
log = Logger().get_logger()

@click.group()
def cloud():
    """Provides access to cloud servers from combahton.net"""

cloud.add_command(reinstall)

@click.command(name="view")
@click.argument("contract", type=click.INT)
@click.option("-f", "--format", "output_format", type=click.Choice(['table','json'], case_sensitive=False), default='table')
def cloud_view(contract, output_format):
    """View details about the specified cloud instance"""
    try:
        response = api.request(component = "kvm", method = "server", action = "view", id = contract)
        if "status" in response:
            res_status = api.parse_status(response["status"])
            if not res_status:
                if output_format == "table":
                    click.echo(tabulate(([k, v] for k, v in response.items())))
                elif output_format == "json":
                    click.echo(response)
            else:
                log.log(res_status["level"], res_status["message"])
    except (ValueError) as error:
        log.error(error)

cloud.add_command(cloud_view)

@click.command(name="stop")
@click.argument("contract", type=click.INT)
def cloud_stop(contract):
    """Stops the specified cloud server"""
    try:
        response = api.request(component = "kvm", method = "server", action = "control", id = contract, command = "stop")
        if "status" in response:
            res_status = api.parse_status(response["status"])
            log.log(res_status["level"], res_status["message"])
        elif "success" in response:
            if isinstance(response["success"], bool):
                if response["success"]:
                    log.info("The specified cloud instance is being stopped.")
                else:
                    log.warn("The specified cloud instance could not be stopped.")
            else:
                log.fatal("An unknown error occured.")
    except (ValueError) as error:
        log.error(error)

cloud.add_command(cloud_stop)

@click.command(name="start")
@click.argument("contract", type=click.INT)
def cloud_start(contract):
    """Starts the specified cloud server"""
    try:
        response = api.request(component = "kvm", method = "server", action = "control", id = contract, command = "start")
        if "status" in response:
            res_status = api.parse_status(response["status"])
            log.log(res_status["level"], res_status["message"])
        elif "success" in response:
            if isinstance(response["success"], bool):
                if response["success"]:
                    log.info("The specified cloud instance is being started.")
                else:
                    log.warn("The specified cloud instance could not be started.")
            else:
                log.fatal("An unknown error occured.")
    except (ValueError) as error:
        log.error(error)

cloud.add_command(cloud_start)

@click.command(name="reset")
@click.argument("contract", type=click.INT)
def cloud_reset(contract):
    """Power-Cycles / Resets the specified cloud server"""
    try:
        response = api.request(component = "kvm", method = "server", action = "control", id = contract, command = "reset")
        if "status" in response:
            res_status = api.parse_status(response["status"])
            log.log(res_status["level"], res_status["message"])
        elif "success" in response:
            if isinstance(response["success"], bool):
                if response["success"]:
                    log.info("The specified cloud instance is being resetted.")
                else:
                    log.warn("The specified cloud instance could not be resetted.")
            else:
                log.fatal("An unknown error occured.")
    except (ValueError) as error:
        log.error(error)

cloud.add_command(cloud_reset)

@click.command(name="vnc")
@click.argument("contract", type=click.INT)
@click.argument("client-address", required=False)
@click.option("--resolve", is_flag=True, default=False, help="Uses ifconfig.me (external service) to automatically resolve the external IPv4 of this machine")
@click.option("-f", "--format", "output_format", type=click.Choice(['table','json'], case_sensitive=False), default='table')
def cloud_vnc(contract, client_address, resolve, output_format):
    """Initiates a VNC connection with the specified cloud server.
    Either provide the IPv4 address of the client, or use --resolve to automatically resolve it using ifconfig.me (external service)"""
    try:
        if not client_address and resolve:
            client_address = ext.resolve_external_ipv4()
        else:
            log.error("You have not specified a client address.")
            return

        response = api.request(component = "kvm", method = "server", action = "control", id = contract, command = "vnc", source = client_address)
        if "success" in response and response["success"]:
            if output_format == "json":
                click.echo(response)
            elif output_format == "table":
                click.echo(tabulate(response.items()))
    except (ValueError) as error:
        log.error(error)

cloud.add_command(cloud_vnc)