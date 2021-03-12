from dotenv import load_dotenv, find_dotenv, dotenv_values
import os

__version__ = "0.0.0"

config = {
    **dotenv_values(find_dotenv()),
    **os.environ
}