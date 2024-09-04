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



class CreateMember(StatesGroup):
    name = State()
    group_id = State()
    
class SeeMember(StatesGroup):
    id = State() 

class DeleteMember(StatesGroup):
    id = State()


class MemberCallback(CallbackData, prefix="member"):
    name: str
    index: int
    telegram_id: int


def generate_members_kb(members:list[dict[str:str]]):
    builder = InlineKeyboardBuilder()
    
    builder.button(text="Add new member",callback_data="add_new_member")
    for index,member in enumerate(members):
        member_cb = MemberCallback(name=member.get("name"),
                                   telegram_id=member.get("telegram_id"),
                                   index=index)
        builder.button(text=member_cb.name,callback_data=member_cb)
    builder.adjust(1,4,3,2,1)
    return builder.as_markup()






@dp.message(Command("see_members"))
async def see_members(message: Message):
    url = BASE_BACKEND_URL + "/members"
    resp = await request_provider(url, method=Method.GET)
    keyboard = generate_members_kb(resp)
    await message.answer("Choose a student:",reply_markup=keyboard)




@dp.message(Command("create_member"))
async def create_member(message: Message, state: FSMContext):
    await message.answer("Enter the name:")
    await state.set_state(CreateMember.name)



@dp.message(CreateMember.name)
async def get_name(message: Message, state: FSMContext):
    url = BASE_BACKEND_URL + "/members"
    name = message.text
    resp = await request_provider(url, method=Method.POST, body_or_params={"name": name,
                                                                           "telegram_id":0,
                                                                           "group_id":1})
    print(f"{resp=}")
    await message.answer("Successfully created")
    await state.clear()
    



@dp.message(Command("delete_members"))
async def delete_members(message: Message):
    url = BASE_BACKEND_URL + "/members"
    await request_provider(url,method=Method.DELETE)
    await message.answer("Successfully deleted")



@dp.message(Command("see_member"))
async def see_member(message: Message,state: FSMContext):
    await message.answer("Enter id:")
    await state.set_state(SeeMember.id)



@dp.message(SeeMember.id)
async def member_name(message: Message,state: FSMContext):
    id = message.text
    url = BASE_BACKEND_URL + f"/members/{id}"
    logger.info(url)
    resp = await request_provider(url, method=Method.GET)
    await state.clear()
    await message.answer(f"{resp}")


@dp.message(Command("update_member"))
async def update_member(message: Message):
    url = BASE_BACKEND_URL + "/members"
    resp = await request_provider(url, method=Method.GET)
    keyboard = generate_members_kb(resp)
    await message.answer("Choose a student to update:",reply_markup=keyboard)



@dp.callback_query(MemberCallback.filter())
async def upd_get_member_id(query: CallbackQuery, callback_data: MemberCallback):
    ...



@dp.message(Command("delete_member"))
async def delete_member(message: Message):
    url = BASE_BACKEND_URL + "/members"
    resp = await request_provider(url, method=Method.GET)
    keyboard = generate_members_kb(resp)
    await message.answer("Choose a student to delete:",reply_markup=keyboard)



@dp.callback_query(MemberCallback.filter())
async def del_get_member_id(query: CallbackQuery, callback_data: MemberCallback):
    url = BASE_BACKEND_URL + "/members/{item_id}"
    id = callback_data.index
    print(id)
    resp = await request_provider(url, method=Method.DELETE, body_or_params={"item_id": id})
    print(resp)
    await query.message.answer("Successfully deleted")