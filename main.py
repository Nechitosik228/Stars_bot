from os import getenv

from dotenv import load_dotenv
from uvicorn import run
import asyncio
from backend import app
from bot import dp, bot



async def run_backend():
    await asyncio.sleep(1.5)
    run(app=app, host=getenv("API_HOST"), port=int(getenv("API_PORT")))


async def run_bot():
    await dp.start_polling(bot)
    return dp


async def main():
    load_dotenv()
    backend_task = asyncio.create_task(run_backend())
    bot_task = asyncio.create_task(run_bot())
    await asyncio.gather(backend_task, bot_task)


if __name__ == "__main__":
    asyncio.run(main())
    # API_HOST = localhost
    # API_PORT = 4141
