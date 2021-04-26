import click

from commands.misc.iso import iso # pylint: disable=import-error,no-name-in-module

from helpers.api import APIv2 # pylint: disable=import-error,no-name-in-module
from helpers.logger import Logger # pylint: disable=import-error,no-name-in-module
from helpers.external import External  # pylint: disable=import-error,no-name-in-module

ext = External()
api = APIv2()
log = Logger().get_logger()

@click.group()
def misc():
    """Provides access to miscellaneous functions"""

misc.add_command(iso)
