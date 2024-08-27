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





@dp.message(Command("see_lessons"))
async def see_lessons(message: Message):
    ...



@dp.message(Command("create_lesson"))
async def create_lesson(message: Message):
    ...



@dp.message(Command("delete_lessons"))
async def delete_lessons(message: Message):
    ...



@dp.message(Command("see_lesson"))
async def see_lesson(message: Message):
    ...



@dp.message(Command("update_lesson"))
async def update_lesson(message: Message):
    ...



@dp.message(Command("delete_lesson"))
async def delete_lesson(message: Message):
    ...