import sys
from os import getenv
from aiogram.fsm.context import FSMContext
import logging
import asyncio
from aiogram.fsm.state import State, StatesGroup
from enum import Enum
from requests import get
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.types import ( 
    KeyboardButton,
    ReplyKeyboardMarkup,
    Message,
    ReactionTypeEmoji
)


BASE_BACKEND_URL =f'http://{getenv("API_HOST")}:{getenv("API_PORT")}'  



class Registration(StatesGroup):
    name = State()
    type = State()



class Lesson(StatesGroup):
    date = State()
    

users = {"Нечитайло Нікіта":{"name": "Нечитайло Нікіта",
                             "type": "Student",
                             "group": "PYTHON_1y_23_03_10_23"},
         "Дементєєв Дмитро":{"name": "Дементєєв Дмитро",
                             "type": "Teacher",
                             "group": "PYTHON_1y_23_03_10_23"}                     }

lessons = {"PYTHON_1y_23_03_10_23":{"lessons":{"01.08.2024":{"members": {"Нечитайло Нікіта": "5",
                                                                        "Леонід Лісовский": "4"}
                                                                                         }}}}


groups = {"PYTHON_1y_23_03_10_23":{"Teacher":"Дементєєв Дмитро",
                                   "Students":["Нечитайло Нікіта",
                                               "Лісовский Леонід",
                                               "Савін Богдан",
                                               "Луценко Данило"
                                               ]
                                   }}


bot = Bot(token="6825649894:AAGQBedlfzs5tWHzTzuWMczE1JRzgMNTNZ0")
Token="6825649894:AAGQBedlfzs5tWHzTzuWMczE1JRzgMNTNZ0"
dp = Dispatcher()






@dp.message(Command('start'))
async def command_start(message: Message,state: FSMContext):
    name = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=f"{message.from_user.first_name}")
            ],
            
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.react([ReactionTypeEmoji(emoji = "👍")])
    await message.answer(f"Hi!\n"
                         f"Write your name for registration:",
                         reply_markup=name)
    await state.set_state(Registration.name)






@dp.message(Registration.name)
async def get_name (message: types.Message, state: FSMContext):
    type_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=f"Student"),
                KeyboardButton(text=f"Teacher"),
            ]   
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await state.update_data(name=message.text)
    await message.answer(f"<b>{message.text}</b>, now tell us are you a student or are you a teacher",
                          reply_markup=type_keyboard)
    await state.set_state(Registration.type)






@dp.message(Registration.type)
async def get_age(message: types.Message, state: FSMContext):
    answer = message.text
    user_id = message.from_user.id
    
    
    data = await state.update_data(type=answer)
    await state.clear()
    name = data.get('name')
    type = data.get('type')
    if name in users:
        user = users.get(name)
        type_check = user.get("type")
        if type_check == type:
            user_repaired = users.pop(name)
            users[user_id] = user_repaired
            await message.answer(f"Registration succesfully ended.\n"
                                     f"Name: {name}\n"
                                     f"Type: {type}")
        else:
            await message.answer(f"You are not:{type}")

    else:
        await message.answer("Sorry,we don't know you:(")





                
@dp.message(Command("see_members"))
async def see_members(message: Message): 
    url = BASE_BACKEND_URL + "/members"
    response = get(url=url)
    data = response.json() 
    print(f"{data=}")
    # chat_id = message.from_user.id
    # user = users.get(chat_id)
    # name = user.get("name")
    # group = user.get("group")
    await message.answer(f"Your group:{data}\nGive the date of the lesson:")
    
    





@dp.message(Lesson.date)
async def get_stars_count(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    user = users.get(chat_id)
    name = user.get("name")
    group = user.get("group")
    date = message.text
    date_check = lessons.get(group).get("lessons")
    if date in date_check:
        lesson = date_check.get(date).get("members")
        if name in lesson:
            star_count = lesson.get(name)
            await message.answer(f"Your star count: {star_count}")
        else: 
            await message.answer("You were not present in the lesson")
    else:
        await message.answer(f"Your group {group}, didn't have any lessons on {date}")







@dp.message(Command("create_lesson"))
async def create_lesson(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    user = users.get(chat_id)
    name = user.get("name")
    group = user.get("group")
    type = user.get("type")
    students = groups.get(group).get("students")
    if type == "Teacher":
        await message.answer(f"Your group:{group}.\nYour students:{students}.\nWrite who was present")
    else:
        await message.answer("This command is only for teachers") 




@dp.message(Command("see_profile"))
async def see_profile(message: Message,state: FSMContext):
    chat_id = message.from_user.id
    user = users.get(chat_id)
    await message.answer(f"{user}")
    






async def main() -> None:
    bot = Bot(Token)
    await dp.start_polling(bot)






if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())



    


