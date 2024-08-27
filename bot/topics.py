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




@dp.message(Command("see_topics"))
async def see_topics(message: Message):
    ...



@dp.message(Command("create_topic"))
async def create_topic(message: Message):
    ...    



@dp.message(Command("delete_topics"))
async def delete_topics(message: Message):
    ...



@dp.message(Command("see_topic"))
async def see_topic(message: Message):
    ...



@dp.message(Command("update_topic"))
async def update_topic(message: Message):
    ...



@dp.message(Command("delete_topic"))
async def delete_topic(message: Message):
    ...