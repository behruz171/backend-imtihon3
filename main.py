from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import re
from database import db_connect, insert, select
TOKEN = '6496054282:AAGzjbIEpCcxtxo7fnfvDQyWy_YrHC3q9Uc'
storage = MemoryStorage()
pattern = re.compile(r'^\+998[0-9]{9}')
pattern1 = re.compile(r'^[0-9]')
pattarn2 = re.compile("[\w.]+@{1}[a-z]+\.[a-z]{2,3}")


bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)

class Partner(StatesGroup):
    name = State()
    phone = State()
    age = State()
    email = State()

async def on_startup(_):
    await db_connect()
    print("Bot ishga tushdi")

async def is_subscribed(user_id):
    chat_id = "@nimadir172"
    try:
        member = await bot.get_chat_member(chat_id, int(user_id))
        if member.status == types.ChatMemberStatus.MEMBER or member.status == types.ChatMemberStatus.CREATOR:
            return True
    except Exception as e:
        print(e)
        return False

@dp.message_handler(commands=['start', 'tekshirish'])
async def start_btn(message: types.Message):
    if await is_subscribed(message.chat.id):
        buttons = ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = KeyboardButton(text="Royxatdan o'tish")
        buttons.add(button1)
        await message.answer(text="Botimizga hush kelibsiz", reply_markup=buttons)
    else:
        buttons = ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = KeyboardButton(text="t.me/nimadir172")
        button2 = KeyboardButton(text="/tekshirish")
        buttons.add(button1, button2)
        await message.answer(text="Botdan kanalga azo bolgandan keyin foydalana olasiz\nhttps://t.me/nimadir172", reply_markup=buttons)

@dp.message_handler(commands=['list'])
async def list_of_aplications(message: types.Message):
    result = ""
    aplications = select()
    for i in aplications:
        result += f'id: {i[0]} name: {i[1]}\n'
    await message.answer(text=result)

@dp.message_handler(Text(equals="Royxatdan o'tish"), state="*")
async def btn1(message: types.Message):
    text = "Botimizga xush kelibsiz\nRoyxatdan o'tish boshlandi\nIsmingizni yozing"
    await message.answer(text=text)
    await Partner.name.set()

@dp.message_handler(state=Partner.name)
async def set_name(message: types.Message, state: FSMContext):
    text = "Telefon raqamingizni yozing"
    await message.answer(text=text)
    await state.update_data(name=message.text)

    await Partner.next()

@dp.message_handler(state=Partner.phone)
async def set_name(message: types.Message, state: FSMContext):
    if pattern.match(message.text):
        text = "Yoshingizni yozing"
        await state.update_data(phone=message.text)
        await message.answer(text=text)

        await Partner.next()
    else:
        await message.answer("Togri telefon yozing")

@dp.message_handler(state=Partner.age)
async def set_name(message: types.Message, state: FSMContext):
    if pattern1.match(message.text):
        text = "emailni kiriting"
        await state.update_data(age=message.text)
        await message.answer(text=text)

        await Partner.next()
    else:
        await message.answer("Yoshingizni kiriting")

@dp.message_handler(state=Partner.email)
async def set_name(message: types.Message, state: FSMContext):
    if pattarn2.match(message.text):
        buttons = ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = KeyboardButton(text="HA")
        button2 = KeyboardButton(text="YOQ")
        buttons.add(button1, button2)
        await state.update_data(email=message.text)

        data = await state.get_data()

        text = f"{data['name']},\n{data['phone']},\n{data['age']},\n{data['email']}\nBarcha malumotlar Tog'rimi"
        await message.answer(text=text, reply_markup=buttons)

        await Partner.next()
    else:
        await message.answer("email kiriting")

@dp.message_handler(Text(equals="HA"))
async def set_aplication(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await insert(data['name'], data['phone'], data['age'], data['email'])
    await state.finish()
    await message.answer("Royxatdan o'tdingiz")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)