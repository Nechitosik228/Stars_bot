from . import (FSMContext,
               request_provider,
               Method,
               State,
               StatesGroup,
               dp,
               BASE_BACKEND_URL,
               Command,
               Message,
               )



class CreateStarsCount(StatesGroup):
    lesson_id = State()
    member_id = State()
    stars_count = State()



class SeeStarsCount(StatesGroup):
    lesson_id = State()
    member_id = State()


class DeleteStarsCount(StatesGroup):
    lesson_id = State()
    member_id = State()


class UpdateStarsCount(StatesGroup):
    lesson_id = State()
    member_id = State()
    star_count = State()
    
    



@dp.message(Command("create_stars_count"))
async def create_stars_count(message:Message,state:FSMContext):
    await message.answer("Enter lesson id:")
    await state.set_state(CreateStarsCount.lesson_id)


@dp.message(CreateStarsCount.lesson_id)
async def lesson_id(message:Message,state:FSMContext):
    lesson_id = message.text
    await state.update_data(lesson_id=lesson_id)
    await message.answer("Enter member id:")
    await state.set_state(CreateStarsCount.member_id)


@dp.message(CreateStarsCount.member_id)
async def member_id(message:Message,state:FSMContext):
    member_id = message.text
    await state.update_data(member_id=member_id)
    await message.answer("Enter star count:")
    await state.set_state(CreateStarsCount.stars_count)


@dp.message(CreateStarsCount.stars_count)
async def stars_count(message:Message,state:FSMContext):
    url = BASE_BACKEND_URL + "/lesson_members"
    stars_count = message.text
    data = await state.update_data(stars_count=stars_count)
    lesson_id = data.get("lesson_id")
    member_id = data.get("member_id")
    resp = await request_provider(url,method=Method.POST,body_or_params={"lesson_id":lesson_id,
                                                                         "member_id":member_id,
                                                                         "stars_count": stars_count})
    print(resp)
    await message.answer("Successfully created")
    await state.clear()
    


@dp.message(Command("see_stars_count"))
async def see_stars(message:Message,state:FSMContext):
    await message.answer("Enter lesson id:")
    await state.set_state(SeeStarsCount.lesson_id)



@dp.message(SeeStarsCount.lesson_id)
async def get_member_id(message:Message,state:FSMContext):
    lesson_id = message.text
    await state.update_data(lesson_id=lesson_id)
    await message.answer("Enter member id:")
    await state.set_state(SeeStarsCount.member_id)

@dp.message(SeeStarsCount.member_id)
async def get_member_id(message:Message,state:FSMContext):
    member_id = message.text
    data = await state.update_data(member_id=member_id)
    lesson_id = data.get("lesson_id")
    url = BASE_BACKEND_URL + f"/lesson_members/{lesson_id}/{member_id}"
    mem_url = BASE_BACKEND_URL + f"/members/{member_id}"
    less_url = BASE_BACKEND_URL + f"/lessons/{lesson_id}"
    less_resp = await request_provider(less_url, method=Method.GET)
    mem_resp = await request_provider(mem_url, method=Method.GET)
    member = mem_resp.get("name")
    lesson= less_resp.get("date")
    resp = await request_provider(url,method=Method.GET)
    print(less_resp)
    print(mem_resp)
    print(resp)
    await message.answer(f"date:{lesson}\nname:{member}\nid:{resp.get('member_id')}\nstars count:{resp.get('stars')}")
    await state.clear()



@dp.message(Command("delete_stars_count_member"))
async def delete_star_count_member(message:Message,state:FSMContext):
    await message.answer("Enter lesson id:")
    await state.set_state(DeleteStarsCount.lesson_id)



@dp.message(DeleteStarsCount.lesson_id)
async def get_lesson_id(message:Message,state:FSMContext):
    lesson_id = message.text
    await state.update_data(lesson_id=lesson_id)
    await message.answer("Enter member id:")
    await state.set_state(DeleteStarsCount.member_id)

@dp.message(DeleteStarsCount.member_id)
async def get_member_id(message:Message,state:FSMContext):
    member_id = message.text
    data = await state.update_data(member_id=member_id)
    lesson_id = data.get("lesson_id")
    url = BASE_BACKEND_URL + f"/lesson_members/{lesson_id}/{member_id}"
    resp = await request_provider(url,method=Method.DELETE)
    print(resp)
    await message.answer("Successfully deleted")
    await state.clear()



@dp.message(Command("update_lesson_member"))
async def upd_lesson_member(message:Message,state:FSMContext):
    await message.answer("Enter lesson id:")
    await state.set_state(UpdateStarsCount.lesson_id)


@dp.message(UpdateStarsCount.lesson_id)
async def upd_lesson_id(message:Message,state:FSMContext):
    lesson_id = message.text
    await state.update_data(lesson_id=lesson_id)
    await message.answer("Enter member id:")
    await state.set_state(UpdateStarsCount.member_id)

@dp.message(UpdateStarsCount.member_id)
async def upd_member_id(message:Message,state:FSMContext):
    member_id = message.text
    await state.update_data(member_id=member_id)
    await message.answer("Enter new star count:")
    await state.set_state(UpdateStarsCount.star_count)



@dp.message(UpdateStarsCount.star_count)
async def upd_star_count(message:Message,state:FSMContext):
    star_count = message.text
    data = await state.update_data(star_count=star_count)
    lesson_id = data.get("lesson_id")
    member_id = data.get("member_id")
    url = BASE_BACKEND_URL + f"/lesson_members/{lesson_id}/{member_id}"
    resp = await request_provider(url,method=Method.PUT, body_or_params={"stars_count":star_count})
    print(resp)
    await message.answer("Successfully updated")
    await state.clear()
