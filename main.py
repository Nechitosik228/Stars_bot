from os import getenv
from dotenv import load_dotenv
from uvicorn import run
from backend import app


if __name__ == "__main__":
    # API_HOST = localhost
    # API_PORT = 4141

    load_dotenv()
    run(app=app, host=getenv("API_HOST"), port=int(getenv("API_PORT")))
