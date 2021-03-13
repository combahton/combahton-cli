import os
from dotenv import find_dotenv, dotenv_values

__version__ = "1.0.0"

config = {
    **dotenv_values(find_dotenv()),
    **os.environ
}
