from os import getenv

from dotenv import load_dotenv
from uvicorn import run
from backend import app


def run_backend():
    run(app=app, host=getenv("API_HOST"), port=int(getenv("API_PORT")))


if __name__ == "__main__":
    load_dotenv()
    run_backend()
    # API_HOST = localhost
    # API_PORT = 4141
