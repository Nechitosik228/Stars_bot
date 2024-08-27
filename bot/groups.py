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






@dp.message(Command("see_groups"))
async def see_groups(message: Message):
    ...



@dp.message(Command("create_group"))
async def create_group(message: Message):
    ...



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