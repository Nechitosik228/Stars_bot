from .. import app_config
from backend.app import Config
from .forms import SeeItem
from os import getenv
from dotenv import load_dotenv




Session = Config.SESSION





load_dotenv()


BASE_BACKEND_URL = f'http://{getenv("API_HOST")}:{getenv("API_PORT")}'

app = app_config.app

from . import (
    auth,
    error_handlers,
    default,
    group,
    lesson,
    member,
    topic,
)
