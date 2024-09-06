
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
               F,
               types)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class DeleteGroup(StatesGroup):
    id = State()


class UpdateGroup(StatesGroup):
    id = State()
    name = State()

class CreateGroup(StatesGroup):
    name = State()


class GroupCallback(CallbackData, prefix="group"):
    name: str
    index: int


class MemberCallback(CallbackData, prefix="member"):
    name: str
    index: int
    telegram_id: int


class SeeGroup(StatesGroup):
    id = State()


def generate_groups_kb(groups:list[dict[str:str]]):
    builder = InlineKeyboardBuilder()
    builder.adjust(1,4,3,2,1)
    builder.button(text="Add new group",callback_data="add_new_group")
    for index,group in enumerate(groups):
        group_cb = GroupCallback(name=group.get("name"),index=index)
        builder.button(text=group_cb.name,callback_data=group_cb)
    return builder.as_markup()


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

@dp.message(Command("all_groups"))
async def see_groups(message: Message):
    url = BASE_BACKEND_URL + "/groups"
    resp = await request_provider(url, method=Method.GET)
    keyboard = generate_groups_kb(resp)
    await message.answer("choose a group:",reply_markup=keyboard)

@dp.callback_query(GroupCallback.filter())
async def get_group_members(query: CallbackQuery,callback_data: GroupCallback):
    url = BASE_BACKEND_URL + "/members"

    resp = await request_provider(url, method=Method.GET,body_or_params={"group_id":callback_data.index})
    keyboard = generate_members_kb(resp)
    await query.message.answer("Choose a student:",reply_markup=keyboard)






@dp.callback_query(MemberCallback.filter())
async def get_member(query: CallbackQuery, callback_data: MemberCallback):
    name = callback_data.name
    kb = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[ 
        [types.InlineKeyboardButton(text="Delete Member", callback_data="del_m")], 
        [types.InlineKeyboardButton(text="Update Member", callback_data="upd_m")], 
        ]) 
    await query.message.answer(f"Name:{name}\nChoose option",reply_markup=kb)

    


@dp.message(Command("create_group"))
async def create_group(message: Message, state:FSMContext):
    await message.answer("Enter name of group:")
    await state.set_state(CreateGroup.name)
@dp.callback_query(F.data.startswith("add_new_topic"))
async def create_group_q(query: CallbackQuery, state: FSMContext):
    await query.message.answer("Enter the name:")
    await state.set_state(CreateGroup.name)

@dp.message(CreateGroup.name)
async def group_name(message: Message,state:FSMContext):
    url = BASE_BACKEND_URL + "/groups"
    name = message.text
    resp = await request_provider(url, method=Method.POST, body_or_params={"name": name})
    print(f"{resp=}")
    await message.answer("Successfully created")
    await state.clear()

@dp.message(Command("delete_all_groups"))
async def delete_groups(message: Message):
    url = BASE_BACKEND_URL + "/groups"
    await request_provider(url,method=Method.DELETE)
    await message.answer("Successfully deleted")



@dp.message(Command("see_one_group"))
async def see_group(message: Message,state:FSMContext):
    await message.answer("Enter id:")
    await state.set_state(SeeGroup.id)


@dp.message(SeeGroup.id)
async def group_name(message: Message,state: FSMContext):
    id = message.text
    url = BASE_BACKEND_URL + f"/groups/{id}"
    resp = await request_provider(url, method=Method.GET)
    kb = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[ 
        [types.InlineKeyboardButton(text="Delete group", callback_data="del_gr")], 
        [types.InlineKeyboardButton(text="Update group", callback_data="upd_gr")], 
        ])
    await message.answer(f'id:{id}\nName:{resp.get("name")}\nchoose option:', reply_markup=kb)
    await state.clear()




@dp.message(Command("update_group"))
async def update_group(message: Message, state: FSMContext):
    await message.answer("Enter id:")
    await state.set_state(UpdateGroup.id)
@dp.callback_query(F.data.startswith("upd_g"))
async def update_group(query: CallbackQuery, state: FSMContext):
    await query.message.answer("Enter id:")
    await state.set_state(UpdateGroup.id)


@dp.message(UpdateGroup.id)
async def upd_get_group_id(message: Message, state: FSMContext):
    id = message.text
    await state.update_data(id=id)
    await message.answer("Enter new name:")
    await state.set_state(UpdateGroup.name)


@dp.message(UpdateGroup.name)
async def upd_get_name(message:Message,state:FSMContext):
    name = message.text
    data = await state.update_data(name=name)
    id = data.get("id")
    url = BASE_BACKEND_URL + f"/groups/{id}"
    resp = await request_provider(url, method=Method.PUT, body_or_params={"name":name})
    print(resp)
    await message.answer(f"Successfully updated:\nName:{name}")
    await state.clear()




@dp.message(Command("delete_one_group"))
async def delete_group(message: Message,state:FSMContext):
    await message.answer("Enter id:")
    await state.set_state(DeleteGroup.id)
@dp.callback_query(F.data.startswith("del_g"))
async def delete_group(query: CallbackQuery,state:FSMContext):
    await query.message.answer("Enter id:")
    await state.set_state(DeleteGroup.id)


@dp.message(DeleteGroup.id)
async def del_get_group_id(message: Message,state:FSMContext):
    id = message.text
    print(id)
    url = BASE_BACKEND_URL + f"/groups/{id}"
    resp = await request_provider(url, method=Method.DELETE)
    print(resp)
    await message.answer("Successfully deleted")
    await state.clear()