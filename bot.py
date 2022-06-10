import requests
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.input_media import InputMediaPhoto
import db

API_TOKEN = '5509187287:AAE8EXqIEGsXCCzBJ-8GbnHeS49UGMRKVUQ'
URL = f'https://api.telegram.org/bot{API_TOKEN}/getMe'

logging.basicConfig(level=logging.INFO)

bot = Bot(API_TOKEN)
dp = Dispatcher(bot)


def user_is_new(user_id):
    db.cur.execute("SELECT sent_messages.user_id from sent_messages")
    users = db.cur.fetchone()
    if users is None:
        return False
    

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi\nI'am Housing bot\nPowerd by aiogram.")


@dp.message_handler(commands=['new'])
async def send_newest_ad(message: types.Message):
    print(message.from_user)
    user_id, username = message.from_user.id, message.from_user.username
    
    if user_is_new(user_id):
        db.init_new_user(user_id, username)
    else:
        print('user initialaized')

    ad = db.fetch_one_from_db()
    await message.answer_photo(ad.photo_url[-1], caption=f'{ad.ad_name}\nЦена:\
 {ad.price}\nАдрес: {ad.address_title}')

@dp.message_handler(commands=['start', 'help'])
async def infinite_notifications(message: types.Message):
    user_id = message.from_user.id


if __name__ == '__main__':
    user_is_new(10)
