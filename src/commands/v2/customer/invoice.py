from datetime import datetime

import click
from tqdm import tqdm
from tabulate import tabulate

from helpers.api import APIv2 # pylint: disable=import-error,no-name-in-module
from helpers.logger import Logger # pylint: disable=import-error,no-name-in-module

api = APIv2()
log = Logger().get_logger()

@click.group()
def invoice():
    """Provides access to invoices"""

@click.command(name="all")
@click.option("-f", "--format", "output_format", type=click.Choice(['table','json'], case_sensitive=False), default='table')
@click.option("-H", "--human-readable", "human", is_flag=True, default=False)
def invoice_all(output_format, human):
    """View all invoices of the specified customer account"""
    try:
        response = api.request(component = "customer", method = "invoices", action = "view_all")
        if "status" in response:
            res_status = api.parse_status(response["status"])
            if res_status:
                log.log(res_status["level"], res_status["message"])
        else:
            if human:
                for k, val in enumerate(response):
                    response[k]["time"] = datetime.utcfromtimestamp(int(val["time"])).strftime('%Y-%m-%d %H:%M:%S UTC')
            if output_format == "table":
                click.echo(tabulate(response, headers="keys"))
            else:
                click.echo(response)
    except (ValueError) as error:
        log.error(error)

invoice.add_command(invoice_all)

@click.command(name="unpaid")
@click.option("-f", "--format", "output_format", type=click.Choice(['table','json'], case_sensitive=False), default='table')
@click.option("-H", "--human-readable", "human", is_flag=True, default=False)
def invoice_unpaid(output_format, human):
    """View unpaid invoices of the specified customer account"""
    try:
        response = api.request(component = "customer", method = "invoices", action = "view_unpaid")
        if "status" in response:
            res_status = api.parse_status(response["status"])
            if res_status:
                log.log(res_status["level"], res_status["message"])
        else:
            if human:
                for k, val in enumerate(response):
                    response[k]["time"] = datetime.utcfromtimestamp(int(val["time"])).strftime('%Y-%m-%d %H:%M:%S UTC')
            if output_format == "table":
                click.echo(tabulate(response, headers="keys"))
            else:
                click.echo(response)
    except (ValueError) as error:
        log.error(error)

invoice.add_command(invoice_unpaid)

@click.command(name="download")
@click.argument("invoice_id", type=click.INT)
@click.argument("file_path", type = click.Path(exists=False, dir_okay=False, allow_dash=False))
def invoice_download(invoice_id, file_path):
    """Download a specific of the specified customer account"""
    try:
        response = api.request(component = "customer", method = "invoices", action = "view", id = invoice_id, stream = True)
        if "status" in response:
            res_status = api.parse_status(response["status"])
            if res_status:
                log.log(res_status["level"], res_status["message"])
        else:
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(4096):
                    file.write(chunk)
    except (ValueError) as error:
        log.error(error)

invoice.add_command(invoice_download)
