from ftplib import FTP
from pathlib import Path
from tqdm import tqdm
import click

from helpers.config import config # pylint: disable=import-error,no-name-in-module
from helpers.logger import Logger # pylint: disable=import-error,no-name-in-module

log = Logger().get_logger()

@click.command(name="iso-upload")
@click.argument("contract", type = click.INT)
@click.argument("image", type = click.Path(exists=True))
@click.argument("password", type = click.STRING, default = config.get("CB_ISOFTP_PWD"))
def iso(contract, password, image ):
    """Cloud: Manage / Upload Private ISO Images
    Either provide the password, or set it inside an environment variable: CB_ISOFTP_PWD"""
    image = Path(image)
    host = "isoshare-ffm2.combahton.net"
    user = "cloud{}".format(contract)
    with FTP(host = host, user = user, passwd = password) as ftp, \
        open(image, 'rb') as file, \
        tqdm(unit = 'B', unit_scale = True, leave = False, miniters = 1, desc = 'Uploading {}...'.format(image.name), total = image.stat().st_size) as tqdm_instance:
        ftp.storbinary(f'STOR {image.name}', file, callback = lambda sent: tqdm_instance.update(len(sent)))
