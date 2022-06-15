import random
import asyncio
import logging
from enum import Enum, auto

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import *

import db
from krishakz_parser import krishakz_scrapper


API_TOKEN = '5509187287:AAE8EXqIEGsXCCzBJ-8GbnHeS49UGMRKVUQ'
URL = f'https://api.telegram.org/bot{API_TOKEN}/getMe'

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("BOT")

bot = Bot(API_TOKEN)
loop = asyncio.get_event_loop()

dp = Dispatcher(bot, loop=loop)
db.init_database()

USERS_TASKS = dict()

def user_is_new(user_id: int) -> bool:
    log.info("INITIALIZING NEW USER")
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
    log.info(messages)
    if (user_id, ad_id) in messages:
        return True
    return False


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

def _format_message(ad: db.DataFromDB):
    title = f'<a href="{ad.url}">{ad.ad_name}</a>'
    formatted_message = f'{title}\nЦена: {ad.price}\n'
    return formatted_message


async def _send_message(message: types.Message, ad):
    user_id, username = message.from_user.id, message.from_user.username
    if message_sent(user_id, ad.ad_id):
        await message.answer('Нет новых объявлений')
        return None
    db.insert_into_sent_messages(user_id, ad.ad_id, username)
    try:
        await message.answer_photo(ad.photo_url[0], caption=_format_message(ad), parse_mode=types.ParseMode.HTML)
    except BadRequest:
        await message.answer(f'{ad.ad_name}\nЦена: {ad.price}\nАдрес: {ad.address_title}\nСсылка: {ad.url}')

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    user_id, username = message.from_user.id, message.from_user.username
    start_buttons = ['Начать', 'Последнее 📢', 'Стоп']
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True) 
    keyboard.add(*start_buttons)
    if user_is_new(user_id):
        #print('initialazing uesr')
        db.init_new_user(user_id, username)
    await message.answer("Hi\nI'am Housing bot\nPowerd by aiogram."\
            , reply_markup=keyboard)

@dp.message_handler(Text(equals='Последнее 📢'))
async def send_newest_ad(message: types.Message):
    ad = db.fetch_one_from_db()
    await _send_message(message, ad)

async def _send_infinite_notifications(message: types.Message, user_id):
    queue = update_queue(user_id)
    while True:
        if not queue:
            queue = update_queue(user_id)
            await asyncio.sleep(5)
        else:
            ad_from_queue = queue.pop()
            await _send_message(message, ad_from_queue)
            await asyncio.sleep(5)

def _create_user_tasks(message: types.Message, user_id):
    my_task = asyncio.create_task(_send_infinite_notifications(message, user_id))
    #print(type(my_task))
    USERS_TASKS.update({user_id: my_task})


@dp.message_handler(Text(equals=['Начать', 'Стоп']))
async def infinite_notifications(message: types.Message):
    user_id = message.from_user.id
    if message.text == 'Начать':
        _create_user_tasks(message, user_id)
    elif message.text == 'Стоп': 
        if USERS_TASKS.get(user_id):
            task = USERS_TASKS.pop(user_id)
            task.cancel()

async def _retrive_data_from_scrapper(_type, rooms, rent_period):
    data = await krishakz_scrapper('arenda', 1, 2) 
    return data

async def update_database():
    #print("process started")
    log.info('updating database')
    while True:
        houses_data = await _retrive_data_from_scrapper('arenda', 1, 2)
        db.insert_into_database(houses_data)
        await asyncio.sleep(random.randint(40, 60))
            
if __name__ == '__main__':
    #log.info(message_sent(741311709, 1))
    dp.loop.create_task(update_database())
    executor.start_polling(dp, skip_updates=True)

