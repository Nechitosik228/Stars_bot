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
               CallbackQuery,
               F,
               types)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData



class CreateTopic(StatesGroup):
    name = State()
    group_id = State()
    


class DeleteTopic(StatesGroup):
    id = State()



class SeeTopic(StatesGroup):
    id = State()


class UpdateTopic(StatesGroup):
    id = State()
    name = State()
    group_id = State()



class TopicCallback(CallbackData, prefix="topic"):
    name: str
    index: int


def generate_topics_kb(topics:list[dict[str:str]]):
    builder = InlineKeyboardBuilder()
    for index,topic in enumerate(topics):
        topic_cb = TopicCallback(name=topic.get("name"),index=index)
        builder.button(text=topic_cb.name,callback_data=topic_cb)
    builder.adjust(4,3,2,1)
    return builder.as_markup()



@dp.message(Command("all_topics"))
async def see_topics(message: Message):
    url = BASE_BACKEND_URL + "/topics"
    resp = await request_provider(url, method=Method.GET)
    keyboard = generate_topics_kb(resp)
    await message.answer("choose topic:",reply_markup=keyboard)



@dp.callback_query(TopicCallback.filter())
async def get_member(query: CallbackQuery, callback_data: TopicCallback):
    name = callback_data.name
    kb = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[ 
        [types.InlineKeyboardButton(text="See lessons", callback_data="see_les")], 
        [types.InlineKeyboardButton(text="Update Topic", callback_data="upd_t")],
        [types.InlineKeyboardButton(text="Delete Topic", callback_data="del_t")] 
        ]) 
    await query.message.answer(f"Name:{name}\nChoose option",reply_markup=kb)



@dp.message(Command("create_topic"))
async def create_topic(message: Message,state: FSMContext):
    await message.answer("Enter name of topic:")
    await state.set_state(CreateTopic.name)
# @dp.callback_query(F.data.startswith("add_new_topic"))
# async def create_topic_q(query: CallbackQuery, state: FSMContext):
#     await query.message.answer("Enter the name:")
#     await state.set_state(CreateTopic.name)




@dp.message(CreateTopic.name)
async def get_topic_name(message: Message,state:FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer("Enter group id:")
    await state.set_state(CreateTopic.group_id)


@dp.message(CreateTopic.group_id)
async def get_tel_id(message:Message,state:FSMContext):
    url = BASE_BACKEND_URL + "/topics"
    group_id = message.text
    data = await state.update_data(group_id=group_id)
    name = data.get("name")
    resp = await request_provider(url, method=Method.POST, body_or_params={"name":name,
                                                                           "group_id": group_id})
    print(resp)
    await message.answer("Successfully created")
    await state.clear()




@dp.message(Command("delete_all_topics"))
async def delete_topics(message: Message):
    url = BASE_BACKEND_URL + "/topics"
    await request_provider(url,method=Method.DELETE)
    await message.answer("Successfully deleted")



@dp.message(Command("see_one_topic"))
async def see_topic(message: Message,state:FSMContext):
    await message.answer("Enter id:")
    await state.set_state(SeeTopic.id)



@dp.message(SeeTopic.id)
async def member_name(message: Message,state: FSMContext):
    id = message.text
    url = BASE_BACKEND_URL + f"/topics/{id}"
    
    resp = await request_provider(url, method=Method.GET)
    kb = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[ 
        [types.InlineKeyboardButton(text="Delete Topic", callback_data="del_t")], 
        [types.InlineKeyboardButton(text="Update Topic", callback_data="upd_t")], 
        ])
    
    await message.answer(f'id:{id}\nName:{resp.get("name")}\ngroup id:{resp.get("group_id")}\nchoose option:', reply_markup=kb)
    await state.clear()


@dp.message(Command("update_topic"))
async def update_topic(message: Message,state:FSMContext):
    await message.answer("Enter id:")
    await state.set_state(UpdateTopic.id)
@dp.callback_query(F.data.startswith("upd_t"))
async def update_topic(query: CallbackQuery, state: FSMContext):
    await query.message.answer("Enter id:")
    await state.set_state(UpdateTopic.id)

@dp.message(UpdateTopic.id)
async def update_name(message:Message,state:FSMContext):
    id = message.text
    await state.update_data(id=id)
    await message.answer("Enter new name:")
    await state.set_state(UpdateTopic.name)

@dp.message(UpdateTopic.name)
async def upd_get_group_id(message:Message, state:FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer("Enter new group id:")
    await state.set_state(UpdateTopic.group_id)


@dp.message(UpdateTopic.group_id)
async def upd_get_tel_id(message:Message,state:FSMContext):
    group_id = message.text
    data = await state.update_data(telegram_id=group_id)
    name = data.get("name")
    id = data.get("id")
    url = BASE_BACKEND_URL + f"/topics/{id}"
    resp = await request_provider(url, method=Method.PUT, body_or_params={"name":name,
                                                                          "group_id": group_id})
    print(resp)
    await message.answer(f"Successfully updated:\nName:{name}\nGroup id:{group_id}")
    await state.clear()



@dp.message(Command("delete_one_topic"))
async def delete_topic(message: Message,state:FSMContext):
    await message.answer("Enter id:")
    await state.set_state(DeleteTopic.id) 
@dp.callback_query(F.data.startswith("del_t"))
async def delete_topic_q(query: CallbackQuery,state:FSMContext):
    await query.message.answer("Enter id:")
    await state.set_state(DeleteTopic.id)

@dp.message(DeleteTopic.id)
async def del_get_member_id(message: Message,state:FSMContext):
    id = message.text
    print(id)
    url = BASE_BACKEND_URL + f"/topics/{id}"
    resp = await request_provider(url, method=Method.DELETE)
    print(resp)
    await message.answer("Successfully deleted")
    await state.clear()