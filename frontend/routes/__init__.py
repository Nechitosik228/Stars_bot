from .. import app_config

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
