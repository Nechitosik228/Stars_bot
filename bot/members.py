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






class Create_Member(StatesGroup):
    name = State()
    telegram_id = State()
    group_id = State()
    role_id = State()






@dp.message(Command("see_members"))
async def see_members(message: Message):
    url = BASE_BACKEND_URL + "/members"
    data = await request_provider(url, method=Method.GET)
    await message.answer(f"Your group:{data}\nGive the date of the lesson:")




@dp.message(Command("create_member"))
async def create_member(message: Message, state: FSMContext):
    await message.answer("Enter the name:")
    await state.set_state(Create_Member.name)



@dp.message(Create_Member.name)
async def get_telegram_id(message: Message, state: FSMContext):
    url = BASE_BACKEND_URL + "/members"
    name = message.text
    
    resp = await request_provider(url, method=Method.POST, body_or_params={"name": name})
    logger.info(f"{resp=}")
    await message.answer(f"very good")





@dp.message(Command("delete_members"))
async def delete_members(message: Message):
    ...



@dp.message(Command("see_member"))
async def see_member(message: Message,state: FSMContext):
    
    await message.answer("Enter id:")
    await state.set_state(Create_Member.telegram_id)

@dp.message(Create_Member.telegram_id)
async def see(message: Message):
    url = url = BASE_BACKEND_URL + "/members/{item_id}"
    id = message.text
    resp = await request_provider(url, method=Method.GET, body_or_params={"item_id": int(id)})
    await message.answer(f"{resp}")


@dp.message(Command("update_member"))
async def update_member(message: Message):
    ...



@dp.message(Command("delete_member"))
async def delete_member(message: Message):
    ...