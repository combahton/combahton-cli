import click
from tabulate import tabulate # pylint: disable=import-error
from helpers.api import APIv2 # pylint: disable=import-error,no-name-in-module
from helpers.logger import Logger # pylint: disable=import-error,no-name-in-module

api = APIv2()
log = Logger().get_logger()

@click.group()
def reinstall():
    """Provides access to reinstall options for cloud servers from combahton.net"""

@click.command(name="list")
@click.option("-f", "--format", "output_format", type=click.Choice(['table','json'], case_sensitive=False), default='table')
def reinstall_list(output_format):
    """List all available reinstallation templates"""
    try:
        response = api.request(component = "kvm", method = "server", action = "reinstall_templates")
        if "status" in response:
            res_status = api.parse_status(response["status"])
            if res_status:
                log.log(res_status["level"], res_status["message"])
        else:
            if output_format == "table":
                click.echo(tabulate(response, headers="keys"))
            elif output_format == "json":
                click.echo(response)
    except (ValueError) as error:
        log.error(error)

reinstall.add_command(reinstall_list)

@click.command(name="execute")
@click.argument("contract", type=click.INT)
@click.argument("template-id", type=click.INT)
def reinstall_exec(contract, template_id):
    """Execute a reinstallation of the specified cloud server"""
    try:
        response = api.request(component = "kvm", method = "server", action = "reinstall", id = contract, template = template_id)
        if "status" in response:
            res_status = api.parse_status(response["status"])
            if res_status:
                log.log(res_status["level"], res_status["message"])
    except (ValueError) as error:
        log.error(error)

reinstall.add_command(reinstall_exec)
