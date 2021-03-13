import click
from tabulate import tabulate

from commands.v2.customer.invoice import invoice # pylint: disable=import-error,no-name-in-module
from commands.v2.customer.contract import contract # pylint: disable=import-error,no-name-in-module

from helpers.api import APIv2 # pylint: disable=import-error,no-name-in-module
from helpers.logger import Logger # pylint: disable=import-error,no-name-in-module

api = APIv2()
log = Logger().get_logger()

@click.group()
def customer():
    """Provides access to customer details from combahton.net"""

customer.add_command(invoice)
customer.add_command(contract)

@click.command(name="credits")
@click.option("-f", "--format", "output_format", type=click.Choice(['table','json','plain'], case_sensitive=False), default='plain')
def customer_credits(output_format):
    """Shows the amount of credits the specified user has in their account"""
    try:
        response = api.request(component = "customer", method = "credits", action = "view")
        if "status" in response:
            res_status = api.parse_status(response["status"])
            if res_status:
                log.log(res_status["level"], res_status["message"])
        else:
            if output_format == "table":
                click.echo(tabulate(([k, v] for k, v in response.items())))
            elif output_format == "json":
                click.echo(response)
            elif output_format == "plain":
                click.echo("{:.2f}".format(float(response["amount"])))
    except (ValueError) as error:
        log.error(error)

customer.add_command(customer_credits)
