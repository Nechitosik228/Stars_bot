import sys
from os import getenv
import logging
import asyncio
from enum import Enum
from aiogram.fsm.context import FSMContext

from dotenv import load_dotenv
from loguru import logger

from . utils import request_provider, Method
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    Message,
    ReactionTypeEmoji,
    CallbackQuery
)


load_dotenv()


BASE_BACKEND_URL = f'http://{getenv("API_HOST")}:{getenv("API_PORT")}'


# class Registration(StatesGroup):
#     name = State()
#     type = State()

bot = Bot(token=getenv("BOT_TOKEN"))
dp = Dispatcher()

async def main() -> None:
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())



from . import lessons,groups,members,topics,roles



# @dp.message(Command("start"))
# async def command_start(message: Message, state: FSMContext):
#     name = ReplyKeyboardMarkup(
#         keyboard=[
#             [KeyboardButton(text=f"{message.from_user.first_name}")],
#         ],
#         resize_keyboard=True,
#         one_time_keyboard=True,
#     )
#     await message.react([ReactionTypeEmoji(emoji="👍")])
#     await message.answer(
#         f"Hi!\n" f"Write your name for registration:", reply_markup=name
#     )
#     await state.set_state(Registration.name)


# @dp.message(Registration.name)
# async def get_name(message: types.Message, state: FSMContext):
#     type_keyboard = ReplyKeyboardMarkup(
#         keyboard=[
#             [
#                 KeyboardButton(text=f"Student"),
#                 KeyboardButton(text=f"Teacher"),
#             ]
#         ],
#         resize_keyboard=True,
#         one_time_keyboard=True,
#     )
#     await state.update_data(name=message.text)
#     await message.answer(
#         f"<b>{message.text}</b>, now tell us are you a student or are you a teacher",
#         reply_markup=type_keyboard,
#     )
#     await state.set_state(Registration.type)


# @dp.message(Registration.type)
# async def get_age(message: types.Message, state: FSMContext):
#     answer = message.text
#     user_id = message.from_user.id

#     data = await state.update_data(type=answer)
#     await state.clear()
#     name = data.get("name")
#     type = data.get("type")
#     if name in users:
#         user = users.get(name)
#         type_check = user.get("type")
#         if type_check == type:
#             user_repaired = users.pop(name)
#             users[user_id] = user_repaired
#             await message.answer(
#                 f"Registration succesfully ended.\n" f"Name: {name}\n" f"Type: {type}"
#             )
#         else:
#             await message.answer(f"You are not:{type}")

#     else:
#         await message.answer("Sorry,we don't know you:(")


