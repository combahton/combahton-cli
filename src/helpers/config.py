import os
from dotenv import find_dotenv, dotenv_values

config = {
    **dotenv_values(find_dotenv()),
    **os.environ
}
