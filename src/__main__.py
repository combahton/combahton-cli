import sys
import click

from commands.v2.antiddos.__main__ import antiddos as antiddos_v2
from commands.v2.cloud.__main__ import cloud as cloud_v2
from commands.v2.customer.__main__ import customer as customer_v2
from commands.v2.ipaddr.__main__ import ipaddr as ipaddr_v2
from commands.misc.__main__ import misc

from helpers.config import config
from helpers.logger import Logger

if not config.get("CB_DEBUG"):
    sys.tracebacklimit = 0

log = Logger().get_logger()

@click.group()
def cli():
    """Simple CLI Interface to interact with combahton Services"""

cli.add_command(misc)

def populate_commands_v2():
    cli.add_command(antiddos_v2, name="antiddos")
    cli.add_command(cloud_v2, name="cloud")
    cli.add_command(customer_v2, name="customer")
    cli.add_command(ipaddr_v2, name="ipaddr")

def populate_commands_v3():
    pass

if config.get("CB_API_VERSION") == "v3":
    populate_commands_v3()
    log.error("Access to APIv3 is not yet implemented.")
else:
    populate_commands_v2()

if __name__ == "__main__":
    cli()
