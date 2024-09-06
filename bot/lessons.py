from . import (logging,
               Enum,
               FSMContext,
               load_dotenv,
               logger,
               request_provider,
               Method,
               State,
               StatesGroup,
               dp,
               BASE_BACKEND_URL,
               Command,
               Message,
               types,
               CallbackQuery,
               F)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
import datetime



class DeleteLesson(StatesGroup):
    id = State()


class SeeLesson(StatesGroup):
    id = State()


class UpdateLesson(StatesGroup):
    id = State()
    date = State()
    topic_id = State()

class LessonCallback(CallbackData, prefix="lesson"):
    date: str
    index: int


class CreateLesson(StatesGroup):
    date = State()
    topic_id = State()



def generate_lessons_kb(lessons:list[dict[str:str]]):
    builder = InlineKeyboardBuilder()
    for index,lesson in enumerate(lessons):
        lesson_cb = LessonCallback(date=lesson.get("date"),index=index)
        builder.button(text=lesson_cb.date,callback_data=lesson_cb)
    builder.adjust(4,3,2,1)
    return builder.as_markup()





@dp.message(Command("all_lessons"))
async def see_lessons(message: Message):
    url = BASE_BACKEND_URL + "/lessons"
    resp = await request_provider(url, method=Method.GET)
    keyboard = generate_lessons_kb(resp)
    await message.answer("Choose a lesson:",reply_markup=keyboard)



@dp.message(Command("create_lesson"))
async def create_lesson(message: Message,state:FSMContext):
    await message.answer("Enter the date in this format:\n2024-09-06 00:00:00")
    await state.set_state(CreateLesson.date)


@dp.message(CreateLesson.date)
async def get_topic_id(message: Message, state: FSMContext):
    date = message.text
    await state.update_data(date=date)
    await message.answer("Enter topic id:")
    await state.set_state(CreateLesson.topic_id)

@dp.message(CreateLesson.topic_id)
async def get_tel_id(message:Message,state:FSMContext):
    url = BASE_BACKEND_URL + "/lessons"
    topic_id = message.text
    data = await state.update_data(topic_id=topic_id)
    print(data)
    date = data.get("date")
    resp = await request_provider(url, method=Method.POST, body_or_params={"date":date,
                                                                           "topic_id":topic_id,
                                                                            })
    print(resp)
    await message.answer("Successfully created")
    await state.clear()

@dp.message(Command("delete_all_lessons"))
async def delete_lessons(message: Message):
    url = BASE_BACKEND_URL + "/lessons"
    await request_provider(url,method=Method.DELETE)
    await message.answer("Successfully deleted")



@dp.message(Command("see_one_lesson"))
async def see_lesson(message: Message,state:FSMContext):
    await message.answer("Enter id:")
    await state.set_state(SeeLesson.id)



@dp.message(SeeLesson.id)
async def member_name(message: Message,state: FSMContext):
    id = message.text
    url = BASE_BACKEND_URL + f"/lessons/{id}"
    
    resp = await request_provider(url, method=Method.GET)
    kb = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[ 
        [types.InlineKeyboardButton(text="Delete Lesson", callback_data="del_l")], 
        [types.InlineKeyboardButton(text="Update Lesson", callback_data="upd_l")], 
        [types.InlineKeyboardButton(text="See Starcounts", callback_data="see_stars")]
        ])
    
    await message.answer(f'id:{id}\nDate:{resp.get("date")}\nTopic id: {resp.get("topic_id")}', reply_markup=kb)
    await state.clear()



@dp.message(Command("update_lesson"))
async def update_lesson(message: Message,state:FSMContext):
    await message.answer("Enter id:")
    await state.set_state(UpdateLesson.id)
@dp.callback_query(F.data.startswith("upd_l"))
async def update_lesson_q(query: CallbackQuery, state: FSMContext):
    await query.message.answer("Enter id:")
    await state.set_state(UpdateLesson.id)


@dp.message(UpdateLesson.id)
async def upd_get_lesson_id(message: Message, state: FSMContext):
    id = message.text
    await state.update_data(id=id)
    await message.answer("Enter new date:")
    await state.set_state(UpdateLesson.date)



@dp.message(UpdateLesson.date)
async def upd_get_date(message:Message, state:FSMContext):
    date = message.text
    await state.update_data(date=date)
    await message.answer("Enter new topic id:")
    await state.set_state(UpdateLesson.topic_id)



@dp.message(UpdateLesson.topic_id)
async def upd_get_top_id(message:Message,state:FSMContext):
    topic_id = message.text
    data = await state.update_data(topic_id=topic_id)
    date = data.get("date")
    id = data.get("id")
    url = BASE_BACKEND_URL + f"/lessons/{id}"
    resp = await request_provider(url, method=Method.PUT, body_or_params={"date":date,
                                                                     "topic_id":topic_id
                                                                     })
    print(resp)
    await message.answer(f"Successfully updated:\nDate:{date}\nTopic id:{topic_id}")
    await state.clear()





@dp.message(Command("delete_one_lesson"))
async def delete_lesson(message: Message,state:FSMContext):
    await message.answer("Enter id:")
    await state.set_state(DeleteLesson.id)
@dp.callback_query(F.data.startswith("del_l"))
async def delete_lesson_q(query: CallbackQuery,state:FSMContext):
    await query.message.answer("Enter id:")
    await state.set_state(DeleteLesson.id)



@dp.message(DeleteLesson.id)
async def del_get_lesson_id(message: Message,state:FSMContext):
    id = message.text
    print(id)
    url = BASE_BACKEND_URL + f"/lessons/{id}"
    resp = await request_provider(url, method=Method.DELETE)
    print(resp)
    await message.answer("Successfully deleted")
    await state.clear()