
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
               ReplyKeyboardMarkup,
               types)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from .members import CreateMember




class Group(StatesGroup):
    name = State()


class GroupCallback(CallbackData, prefix="group"):
    name: str
    index: int


class MemberCallback(CallbackData, prefix="member"):
    name: str
    index: int
    telegram_id: int


def generate_groups_kb(groups:list[dict[str:str]]):
    builder = InlineKeyboardBuilder()
    builder.adjust(4,3,2,1)
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

@dp.message(Command("see_groups"))
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


@dp.callback_query(F.data.startswith("add_new_member"))
async def get_member(query: CallbackQuery,state: FSMContext):
    await query.message.answer("Write the name of the student")
    await state.set_state(CreateMember.name)


@dp.callback_query(MemberCallback.filter())
async def get_member(query: CallbackQuery, callback_data: MemberCallback):
    
    name = callback_data.name
    id = callback_data.index
    print(name)
    kb = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[ 
        [types.InlineKeyboardButton(text="Delete Member", callback_data="del_m")], 
        [types.InlineKeyboardButton(text="Update Member", callback_data="upd_m")], 
        ]) 
                        
                       
    await query.message.answer(f"Name:{name}\nid:{id}\nChoose option",reply_markup=kb)

    


@dp.message(Command("create_group"))
async def create_group(message: Message, state:FSMContext):
    await message.answer("Enter name of group:")
    await state.set_state(Group.name)

@dp.message(Group.name)
async def group_name(message: Message,state:FSMContext):
    url = BASE_BACKEND_URL + "/groups"
    name = message.text
    resp = await request_provider(url, method=Method.POST, body_or_params={"name": name})
    print(f"{resp=}")
    await message.answer("Successfully created")
    await state.clear()

@dp.message(Command("delete_groups"))
async def delete_groups(message: Message):
    ...



@dp.message(Command("see_group"))
async def see_group(message: Message):
    ...



@dp.message(Command("update_group"))
async def update_group(message: Message):
    ...



@dp.message(Command("delete_group"))
async def delete_group(message: Message):
    ...