from . import (FSMContext,
               
               request_provider,
               Method,
               State,
               StatesGroup,
               dp,
               BASE_BACKEND_URL,
               Command,
               Message,
               CallbackQuery,
               types,
               F)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData



class CreateMember(StatesGroup):
    name = State()
    group_id = State()
    telegram_id = State()
    
class SeeMember(StatesGroup):
    id = State() 

class DeleteMember(StatesGroup):
    id = State()


class MemberCallback(CallbackData, prefix="member"):
    name: str
    index: int
    


class UpdateMember(StatesGroup):
    id = State()
    name = State()
    group_id = State()
    telegram_id = State()



def generate_members_kb(members:list[dict[str:str]]):
    builder = InlineKeyboardBuilder()
    
    builder.button(text="Add new member",callback_data="add_new_member")
    for index,member in enumerate(members):
        member_cb = MemberCallback(name=member.get("name"),index=index)
        builder.button(text=member_cb.name,callback_data=member_cb)
    builder.adjust(1,4,3,2,1)
    return builder.as_markup()





@dp.message(Command("all_members"))
async def see_members(message: Message):
    url = BASE_BACKEND_URL + "/members"
    resp = await request_provider(url, method=Method.GET)
    keyboard = generate_members_kb(resp)
    await message.answer("Choose a student:",reply_markup=keyboard)




@dp.message(Command("create_member"))
async def create_member(message: Message, state: FSMContext):
    await message.answer("Enter the name:")
    await state.set_state(CreateMember.name)
@dp.callback_query(F.data.startswith("add_new_member"))
async def create_member_q(query: CallbackQuery, state: FSMContext):
    await query.message.answer("Enter the name:")
    await state.set_state(CreateMember.name)



@dp.message(CreateMember.name)
async def get_name(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer("Enter group id:")
    await state.set_state(CreateMember.group_id)


@dp.message(CreateMember.group_id)
async def get_group_id(message:Message, state:FSMContext):
    group_id = message.text
    await state.update_data(group_id=group_id)
    await message.answer("Enter telegram id")
    await state.set_state(CreateMember.telegram_id)


@dp.message(CreateMember.telegram_id)
async def get_tel_id(message:Message,state:FSMContext):
    url = BASE_BACKEND_URL + "/members"
    tel_id = message.text
    data = await state.update_data(telegram_id=tel_id)
    print(data)
    name = data.get("name")
    group_id = data.get("group_id")
    resp = await request_provider(url, method=Method.POST, body_or_params={"name":name,
                                                                     "telegram_id":tel_id,
                                                                     "group_id": group_id})
    print(resp)
    await message.answer("Successfully created")
    await state.clear()





@dp.message(Command("delete_all_members"))
async def delete_members(message: Message):
    url = BASE_BACKEND_URL + "/members"
    await request_provider(url,method=Method.DELETE)
    await message.answer("Successfully deleted")



@dp.message(Command("see_one_member"))
async def see_member(message: Message,state: FSMContext):
    await message.answer("Enter id:")
    await state.set_state(SeeMember.id)



@dp.message(SeeMember.id)
async def member_name(message: Message,state: FSMContext):
    id = message.text
    url = BASE_BACKEND_URL + f"/members/{id}"
    
    resp = await request_provider(url, method=Method.GET)
    kb = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[ 
        [types.InlineKeyboardButton(text="Delete Member", callback_data="del_m")], 
        [types.InlineKeyboardButton(text="Update Member", callback_data="upd_m")], 
        ])
    
    await message.answer(f'id:{id}\nName:{resp.get("name")}\ntelegram id:{resp.get("telegram_id")}\ngroup id:{resp.get("group_id")}\nchoose option:', reply_markup=kb)
    await state.clear()

@dp.message(Command("update_member"))
async def update_member(message: Message, state: FSMContext):
    await message.answer("Enter id:")
    await state.set_state(UpdateMember.id)
@dp.callback_query(F.data.startswith("upd_m"))
async def update_member(query: CallbackQuery, state: FSMContext):
    await query.message.answer("Enter id:")
    await state.set_state(UpdateMember.id)



@dp.message(UpdateMember.id)
async def upd_get_member_id(message: Message, state: FSMContext):
    id = message.text
    await state.update_data(id=id)
    await message.answer("Enter new name:")
    await state.set_state(UpdateMember.name)


@dp.message(UpdateMember.name)
async def upd_get_name(message:Message, state:FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer("Enter new group id:")
    await state.set_state(UpdateMember.group_id)


@dp.message(UpdateMember.group_id)
async def upd_get_group_id(message:Message,state:FSMContext):
    group_id = message.text
    await state.update_data(group_id=group_id)
    await message.answer("Enter new telegram id:")
    await state.set_state(UpdateMember.telegram_id)
    

@dp.message(UpdateMember.telegram_id)
async def upd_get_tel_id(message:Message,state:FSMContext):
    tel_id = message.text
    data = await state.update_data(telegram_id=tel_id)
    name = data.get("name")
    group_id = data.get("group_id")
    id = data.get("id")
    url = BASE_BACKEND_URL + f"/members/{id}"
    resp = await request_provider(url, method=Method.PUT, body_or_params={"name":name,
                                                                     "telegram_id":tel_id,
                                                                     "group_id": group_id})
    print(resp)
    await message.answer(f"Successfully updated:\nName:{name}\nGroup id:{group_id}\nTelegram id:{tel_id}")
    await state.clear()

    
@dp.message(Command("delete_one_member"))
async def delete_member(message: Message,state:FSMContext):
    await message.answer("Enter id:")
    await state.set_state(DeleteMember.id)
@dp.callback_query(F.data.startswith("del_m"))
async def delete_member_q(query: CallbackQuery,state:FSMContext):
    await query.message.answer("Enter id:")
    await state.set_state(DeleteMember.id)


@dp.message(DeleteMember.id)
async def del_get_member_id(message: Message,state:FSMContext):
    id = message.text
    print(id)
    url = BASE_BACKEND_URL + f"/members/{id}"
    resp = await request_provider(url, method=Method.DELETE)
    print(resp)
    await message.answer("Successfully deleted")
    await state.clear()