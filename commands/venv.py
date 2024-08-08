from . import StrEnum


class VenvCommands(StrEnum):
    DEACTIVATE = "deactivate"
    CREATE = "python3 -m venv .venv"
    ACTIVATE = ". ./.venv/bin/activate"
    INSTALL_REQUIREMENTS = "./.venv/bin/pip install -r requirements.txt"
    # RUN_MAIN = "./.venv/bin/python3 main.py"