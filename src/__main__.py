import click
import sys

from helpers.logger import Logger
from helpers.api import APIv2

if getattr(sys, "frozen", False):
    sys.tracebacklimit = 0

log = Logger().getLogger()

api = APIv2()

api.request(kek = "test")