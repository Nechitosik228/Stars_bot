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
               Message)



class CreateMember(StatesGroup):
    name = State()
    group_id = State()
    
class SeeMember(StatesGroup):
    id = State() 

@dp.message(Command("see_members"))
async def see_members(message: Message):
    ...




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
    



    
       





@dp.message(Command("delete_members"))
async def delete_members(message: Message):
    ...



@dp.message(Command("see_member"))
async def see_member(message: Message,state: FSMContext):
    
    await message.answer("Enter id:")
    await state.set_state(SeeMember.id)



@dp.message(SeeMember.id)
async def member_name(message: Message):
    url = BASE_BACKEND_URL + "/members{item_id}"
    id = message.text
    resp = await request_provider(url, method=Method.POST, body_or_params={"item_id": id})



@dp.message(Command("update_member"))
async def update_member(message: Message):
    ...



@dp.message(Command("delete_member"))
async def delete_member(message: Message):
    ...