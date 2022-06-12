import random
import asyncio
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text
#from aiogram.types.input_media import InputMediaPhoto
from aiogram.utils.exceptions import *

import db
from krishakz_parser import krishakz_scrapper


API_TOKEN = '5509187287:AAE8EXqIEGsXCCzBJ-8GbnHeS49UGMRKVUQ'
URL = f'https://api.telegram.org/bot{API_TOKEN}/getMe'

logging.basicConfig(level=logging.INFO)

bot = Bot(API_TOKEN)
loop = asyncio.new_event_loop()
dp = Dispatcher(bot, loop=loop)

db.init_database()

def user_is_new(user_id: int) -> bool:
    db.cur.execute("SELECT sent_messages.user_id FROM sent_messages")
    users = db.cur.fetchall()
    if users is None:
        return False
    elif user_id not in users:
        return False
    return True

def message_sent(user_id, ad_id) -> bool:
    db.cur.execute(f"SELECT user_id, ad_id FROM sent_messages WHERE user_id = {user_id}")
    messages = db.cur.fetchall()
    print(messages)
    if (user_id, ad_id) in messages:
        return True
    return False

def format_message():
    pass

def update_queue(user_id: int) -> list:
    queue = []
    db.cur.execute(f"SELECT user_id, ad_id FROM sent_messages WHERE user_id = {user_id}")
    sent_messages = db.cur.fetchall()
    ads = db.fetch_all_from_db()
    for ad in ads:
        if (user_id, ad.ad_id) in sent_messages:
            continue
        queue.append(ad)
    return queue

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    user_id, username = message.from_user.id, message.from_user.username
    start_buttons = ['Начать', 'Последнее 📢', 'Стоп']
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True) 
    keyboard.add(*start_buttons)
    if user_is_new(user_id):
        print('initialazing uesr')
        db.init_new_user(user_id, username)
    await message.answer("Hi\nI'am Housing bot\nPowerd by aiogram."\
            , reply_markup=keyboard)

@dp.message_handler(Text(equals='Последнее 📢'))
async def send_newest_ad(message: types.Message):
    user_id, username = message.from_user.id, message.from_user.username
    ad = db.fetch_one_from_db()
    print(user_id, username)
    if message_sent(user_id, ad.ad_id):
        await message.answer('Нет новых объявлений')
        return None
    try:
        await message.answer_photo(ad.photo_url[-1], caption=f'{ad.ad_name}\n\
Цена: {ad.price}\nАдрес: {ad.address_title}')
    except BadRequest:
        await message.answer(f'{ad.ad_name}\nЦена: {ad.price}\nАдрес: {ad.address_title}\nСсылка: {ad.url}')
    await asyncio.sleep(5)
    await message.answer_photo(ad.photo_url[-1], caption=f'{ad.ad_name}\nЦена:\
        {ad.price}\nАдрес: {ad.address_title}')
    db.insert_into_sent_messages(user_id, ad.ad_id, username)

@dp.message_handler(Text(equals=['Начать', 'Стоп']))
async def infinite_notifications(message: types.Message):
    user_id, username = message.from_user.id, message.from_user.username
    notifications = False if message.text == 'Стоп' else True
    queue = update_queue(user_id)
    while True:
        print(f'----> QUEUE LEN: {len(queue)}')
        print(f'----> NOTIFICATIONS : {notifications}')
        if notifications is False:
            print('exiting infinite loop')
            break
        if not queue:
            queue = update_queue(user_id)
        ad_from_queue = queue.pop()
        try:
            await message.answer_photo(ad_from_queue.photo_url[0], caption=f'{ad_from_queue.ad_name}\n\
    Цена: {ad_from_queue.price}\nАдрес: {ad_from_queue.address_title}')
        except BadRequest:
            await message.answer(f'{ad_from_queue.ad_name}\nЦена: {ad_from_queue.price}\nАдрес: {ad_from_queue.address_title}\nСсылка: {ad_from_queue.url}')
        await asyncio.sleep(5)
        db.insert_into_sent_messages(user_id, ad_from_queue.ad_id, username)

async def _retrive_data_from_scrapper(_type, rooms, rent_period):
    data = await krishakz_scrapper('arenda', 1, 2) 
    return data

async def update_database():
    print('updating database')
    while True:
        houses_data = await _retrive_data_from_scrapper('arenda', 1, 2)
        db.insert_into_database(houses_data)
        await asyncio.sleep(random.randint(40, 60))
            
if __name__ == '__main__':
    #print(message_sent(741311709, 1))
    #dp.loop.create_task(update_database())
    executor.start_polling(dp, skip_updates=True)

