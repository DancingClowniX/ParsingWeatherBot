import time
import os
from dotenv import load_dotenv
import aiogram.enums
from aiogram import Bot, Dispatcher,types,F
from aiogram.filters import Command
import asyncio
from aiogram import MagicFilter
from aiogram.fsm.storage.memory import MemoryStorage
from bs4 import BeautifulSoup
import requests
from translate import Translator

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Погода по населённому пункту")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Введите данные"
    )
    await message.answer("Начнем", reply_markup=keyboard)

@dp.message(lambda message: message.text.lower() == "погода по населённому пункту")
async def without_puree(message: types.Message):
    await message.answer("Введите населённый пункт")
    @dp.message()
    async def get_weather(message:types.Message):
        print(message.text,message.chat.username,message.chat.first_name)
        translator = Translator(from_lang='ru', to_lang="en")
        translation = translator.translate(str(message.text)).replace(" ","")
        print(translation.lower())
        time.sleep(1)
        url = f'https://www.ventusky.com/ru/{translation.lower()}'
        time.sleep(1)
        response = requests.get(url)
        time.sleep(1)
        soup = BeautifulSoup(response.text, 'html.parser')
        total = str(soup.find(class_='temperature'))[74:81]
        await message.answer(total)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())