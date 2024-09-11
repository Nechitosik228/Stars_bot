import logging
from os import getenv
import sys
from loguru import logger
from dotenv import load_dotenv
from uvicorn import run, Server, Config
import asyncio
from backend import app
from bot import dp, bot



async def run_backend():
    config = Config(app=app, host=getenv("API_HOST"), port=int(getenv("API_PORT")))
    server = Server(config)
    await server.serve()


async def run_bot():
    logger.info("Bot starting")
    await dp.start_polling(bot)


async def main():
    # logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    load_dotenv()
    backend_task = asyncio.create_task(run_backend())
    bot_task = asyncio.create_task(run_bot())
    await asyncio.gather(backend_task, bot_task)


if __name__ == "__main__":
    asyncio.run(main())
    
    # API_HOST = localhost
    # API_PORT = 4141
