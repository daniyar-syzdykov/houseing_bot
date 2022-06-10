import requests
import logging
from aiogram import Bot, Dispatcher, executor, types
import db

API_TOKEN = '5509187287:AAE8EXqIEGsXCCzBJ-8GbnHeS49UGMRKVUQ'
URL = f'https://api.telegram.org/bot{API_TOKEN}/getMe'

logging.basicConfig(level=logging.INFO)

bot = Bot(API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi\nI'am Housing bot\nPowerd by aiogram.")


@dp.message_handler(commands=['/new'])
async def echo(message: types.Message):
    houses = db.read_from_db()
    await message.reply(houses)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
