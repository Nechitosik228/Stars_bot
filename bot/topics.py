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
               CallbackQuery)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData



class Topic(StatesGroup):
    name = State()




class DeleteTopic(StatesGroup):
    id = State()



class UpdateTopic(StatesGroup):
    id = State()



class TopicCallback(CallbackData, prefix="topic"):
    name: str
    index: int


def generate_topics_kb(topics:list[dict[str:str]]):
    builder = InlineKeyboardBuilder()
    builder.adjust(4,3,2,1)
    for index,topic in enumerate(topics):
        topic_cb = TopicCallback(name=topic.get("name"),index=index)
        builder.button(text=topic_cb.name,callback_data=topic_cb)
    return builder.as_markup()



@dp.message(Command("see_topics"))
async def see_topics(message: Message):
    url = BASE_BACKEND_URL + "/topics"
    resp = await request_provider(url, method=Method.GET)
    keyboard = generate_topics_kb(resp)
    await message.answer("choose topic:",reply_markup=keyboard)




@dp.message(Command("create_topic"))
async def create_topic(message: Message,state: FSMContext):
    await message.answer("Enter name of topic:")
    await state.set_state(Topic.name)


@dp.message(Topic.name)
async def get_topic_name(message: Message,state:FSMContext):
    url = BASE_BACKEND_URL + "/topics"
    name = message.text
    resp = await request_provider(url, method=Method.POST, body_or_params={"name":name,
                                                                           "group_id":1})
    print(resp)
    await message.answer("Successfully created")
    await state.clear()



@dp.message(Command("delete_topics"))
async def delete_topics(message: Message):
    ...



@dp.message(Command("see_topic"))
async def see_topic(message: Message):
    ...



@dp.message(Command("update_topic"))
async def update_topic(message: Message,state:FSMContext):
    await message.answer("Enter topic id")
    await state.set_state(UpdateTopic.id)


@dp.message(UpdateTopic.id)
async def update_topic_id(message:Message,state:FSMContext):
    url = BASE_BACKEND_URL
    id = message.text
    int_id = id.isdigit()
    resp = await request_provider(url, method=Method.DELETE, body_or_params={"item_id":int_id})
    print(resp)
    await message.answer("Successfully deleted")
    await state.clear()



@dp.message(Command("delete_topic"))
async def delete_topic(message: Message):
    url = BASE_BACKEND_URL + "/topics"
    resp = await request_provider(url, method=Method.GET)
    keyboard = generate_topics_kb(resp)
    await message.answer("Choose topic to delete:",reply_markup=keyboard)


@dp.callback_query(TopicCallback.filter())
async def delete_topic_id(query:CallbackQuery,callback_data: TopicCallback):
    url = BASE_BACKEND_URL
    id = callback_data.index
    resp = await request_provider(url, method=Method.DELETE, body_or_params={"item_id":id})
    print(resp)
    await query.message.answer("Successfully deleted")