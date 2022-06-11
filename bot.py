import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher, executor, types
#from aiogram.types.input_media import InputMediaPhoto
from aiogram.utils.exceptions import *

import db
from krishakz_parser import krishakz_scrapper


API_TOKEN = '5509187287:AAE8EXqIEGsXCCzBJ-8GbnHeS49UGMRKVUQ'
URL = f'https://api.telegram.org/bot{API_TOKEN}/getMe'

logging.basicConfig(level=logging.INFO)

bot = Bot(API_TOKEN)
dp = Dispatcher(bot)

def user_is_new(user_id: int) -> bool:
    db.cur.execute("SELECT sent_messages.user_id FROM sent_messages")
    users = db.cur.fetchall()
    if users is None:
        return False
    elif user_id not in users:
        return False
    return True

def message_sent(user_id, ad_id):
    db.cur.execute("SELECT user_id, ad_id FROM sent_messages")
    messages = db.cur.fetchall()
    if (user_id, ad_id) in messages:
        return True
    return False

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi\nI'am Housing bot\nPowerd by aiogram.")

@dp.message_handler(commands=['new'])
async def send_newest_ad(message: types.Message):
    user_id, username = message.from_user.id, message.from_user.username
    ad = db.fetch_one_from_db()
    print(user_id, username)

    if user_is_new(user_id):
        print('initialazing uesr')
        db.init_new_user(user_id, username)

    if message_sent(user_id, ad.ad_id):
        await message.answer('There is no new ads')
        return None

    await message.answer_photo(ad.photo_url[-1], caption=f'{ad.ad_name}\nЦена:\
        {ad.price}\nАдрес: {ad.address_title}')
    db.insert_into_sent_messages(user_id, ad.ad_id, username)

@dp.message_handler(commands=['noti'])
async def infinite_notifications(message: types.Message):
    user_id, username = message.from_user.id, message.from_user.username
    queue = []
    if user_is_new(user_id):
        print('initialazing uesr')
        db.init_new_user(user_id, username)
    while True:
        ads = db.fetch_all_from_db()
        print(len(ads))
        for ad in ads:
            if message_sent(user_id, ad.ad_id):
                continue
            try:
                await message.answer_photo(ad.photo_url[-1], caption=f'{ad.ad_name}\n\
 Цена: {ad.price}\nАдрес: {ad.address_title}')
            except BadRequest:
                await message.answer(f'{ad.ad_name}\nЦена: {ad.price}\nАдрес: {ad.address_title}\nСсылка: {ad.url}')
            await asyncio.sleep(5)
            db.insert_into_sent_messages(user_id, ad.ad_id, username)

def _save_data_to_database(data):
    db.insert_into_database(data)

def _retrive_data_from_scrapper(_type, rooms, rent_period):
    data = krishakz_scrapper('arenda', 1, 2) 
    return data

async def update_database():
    houses_data = asyncio.run(_retrive_data_from_scrapper('arenda', 1, 2))
    _save_data_to_database(houses_data)


async def _update_database():
    pass

if __name__ == '__main__':
    asyncio.run(update_database())
    executor.start_polling(dp, skip_updates=True)
