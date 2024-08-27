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




@dp.message(Command("see_roles"))
async def see_roles(message: Message):
    ...



@dp.message(Command("create_role"))
async def create_role(message: Message):
    ...



@dp.message(Command("delete_roles"))
async def delete_roles(message: Message):
    ...



@dp.message(Command("see_role"))
async def see_role(message: Message):
    ...



@dp.message(Command("update_role"))
async def see_roles(message: Message):
    ...



@dp.message(Command("delete_role"))
async def see_roles(message: Message):
    ...