from datetime import datetime

import click
from tabulate import tabulate # pylint: disable=import-error

from helpers.api import APIv2 # pylint: disable=import-error,no-name-in-module
from helpers.logger import Logger # pylint: disable=import-error,no-name-in-module

api = APIv2()
log = Logger().get_logger()

def confirm_callback(ctx, param, value):
    if not param or not value:
        ctx.abort()

@click.group()
def contract():
    """Provides access to contracts"""

@click.command(name="all")
@click.option("-f", "--format", "output_format", type=click.Choice(['table','json'], case_sensitive=False), default='table')
@click.option("-H", "--human-readable", "human", is_flag=True, default=False)
def contract_all(output_format, human):
    """View all contracts of the specified customer account"""
    try:
        response = api.request(component = "customer", method = "contract", action = "view_all")
        if "status" in response:
            res_status = api.parse_status(response["status"])
            if res_status:
                log.log(res_status["level"], res_status["message"])
        else:
            if human:
                for k, val in enumerate(response):
                    response[k]["ordered_time"] = datetime.utcfromtimestamp(int(val["ordered_time"])).strftime('%Y-%m-%d %H:%M:%S UTC')
                    response[k]["lifetime"] = datetime.utcfromtimestamp(int(val["lifetime"])).strftime('%Y-%m-%d %H:%M:%S UTC')
            if output_format == "table":
                click.echo(tabulate(response, headers="keys"))
            else:
                click.echo(response)
    except (ValueError) as error:
        log.error(error)

contract.add_command(contract_all)

@click.command(name="single")
@click.argument("contract_id", type=click.INT)
@click.option("-f", "--format", "output_format", type=click.Choice(['table','json'], case_sensitive=False), default='table')
@click.option("-H", "--human-readable", "human", is_flag=True, default=False)
def contract_single(contract_id, output_format, human):
    """View details about the provided contract"""
    try:
        response = api.request(component = "customer", method = "contract", action = "view", id = contract_id)
        if "status" in response:
            res_status = api.parse_status(response["status"])
            if res_status:
                log.log(res_status["level"], res_status["message"])
        else:
            if human:
                response["ordered_time"] = datetime.utcfromtimestamp(int(response["ordered_time"])).strftime('%Y-%m-%d %H:%M:%S UTC')
                response["lifetime"] = datetime.utcfromtimestamp(int(response["lifetime"])).strftime('%Y-%m-%d %H:%M:%S UTC')
            if output_format == "table":
                click.echo(tabulate(([k, v] for k, v in response.items())))
            else:
                click.echo(response)
    except (ValueError) as error:
        log.error(error)

contract.add_command(contract_single)

@click.command(name="extend")
@click.argument("contract_id", type=click.INT)
def contract_extend(contract_id):
    """Extend the specified contract"""
    try:
        response = api.request(component = "customer", method = "contract", action = "extend", id = contract_id)
        if "status" in response:
            res_status = api.parse_status(response["status"])
            if res_status:
                log.log(res_status["level"], res_status["message"])
    except (ValueError) as error:
        log.error(error)

contract.add_command(contract_extend)

@click.command(name="auto-extend")
@click.argument("contract_id", type=click.INT)
@click.argument("toggle", type=click.BOOL)
def contract_autoextend(contract_id, toggle):
    """Toggle auto-extend of the specified contract"""
    try:
        switch = "enable" if toggle else "disable"
        response = api.request(component = "customer", method = "contract", action = "autoextend", id = contract_id, switch = switch)
        if "status" in response:
            res_status = api.parse_status(response["status"])
            if res_status:
                log.log(res_status["level"], res_status["message"])
    except (ValueError) as error:
        log.error(error)

contract.add_command(contract_autoextend)



@click.command(name="order")
@click.argument("product_id", type=click.INT)
@click.option("--yes", is_flag=True, callback=confirm_callback, expose_value=False, prompt="Do you really want to execute this order?")
def contract_create(product_id):
    """Creates an order for the specified product"""
    try:
        response = api.request(component = "customer", method = "contract", action = "order", id = product_id)
        if "status" in response:
            res_status = api.parse_status(response["status"])
            if res_status:
                log.log(res_status["level"], res_status["message"])
    except (ValueError) as error:
        log.error(error)

contract.add_command(contract_create)
