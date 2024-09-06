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



@dp.message(Command("start"))
async def command_start(message: Message):
    kb = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[ 
        [types.InlineKeyboardButton(text="Member commands", callback_data="mem_com")], 
        [types.InlineKeyboardButton(text="Group commands", callback_data="grp_com")],
        [types.InlineKeyboardButton(text="Lessons commands", callback_data="les_com")],
        [types.InlineKeyboardButton(text="Topics commands", callback_data="top_com")],
        [types.InlineKeyboardButton(text="Roles commands", callback_data="rol_com")],
        ])
    await message.answer("Hello, our user)\nHere's our menu\nChoose what you want to see:",reply_markup=kb)



@dp.callback_query(F.data.startswith("mem_"))
async def member_commands(query:CallbackQuery):
    await query.message.answer("/create_member\n/all_members\n/see_one_member\n/delete_all_members\n/update_member\n/delete_one_member")



@dp.callback_query(F.data.startswith("grp_"))
async def group_commands(query:CallbackQuery):
    await query.message.answer("/create_group\n/all_groups\n/see_one_group\n/delete_all_groups\n/update_group\n/delete_one_group")



@dp.callback_query(F.data.startswith("top_"))
async def group_commands(query:CallbackQuery):
    await query.message.answer("/create_topic\n/all_topics\n/see_one_topic\n/delete_all_topics\n/update_topic\n/delete_one_topic")



@dp.callback_query(F.data.startswith("rol_"))
async def group_commands(query:CallbackQuery):
    await query.message.answer("/create_role\n/all_roles\n/see_one_role\n/delete_all_roles\n/update_role\n/delete_one_role")


@dp.callback_query(F.data.startswith("les_"))
async def group_commands(query:CallbackQuery):
    await query.message.answer("/create_lesson\n/all_lessons\n/see_one_lesson\n/delete_all_lessons\n/update_lesson\n/delete_one_lesson")