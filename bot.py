import random
import asyncio
import logging
import datetime as dt

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import *

import db
from krishakz_parser import krishakz_scrapper


API_TOKEN = '5509187287:AAE8EXqIEGsXCCzBJ-8GbnHeS49UGMRKVUQ'
URL = f'https://api.telegram.org/bot{API_TOKEN}/getMe'

#logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("BOT")

bot = Bot(API_TOKEN)
loop = asyncio.get_event_loop()

dp = Dispatcher(bot, loop=loop)
db.init_database()

USERS_TASKS = dict()

def _format_message(ad: db.DataFromDB):
    title = f'<a href="{ad.url}">{ad.ad_name}</a>'
    formatted_message = f'{title}\nЦена: {ad.price}\n'
    return formatted_message

async def _send_message(message: types.Message, ad):
    user_id, username = message.from_user.id, message.from_user.username
    message_sent = db.message_sent(user_id, ad.ad_id)
    #log.info(f"_send_message MESSAGE SEND IS {message_sent})")
    if db.user_is_new(user_id):
        #log.info("_send_message INITIALIAZING NEW USER")
        db.init_new_user(user_id, username)
    if message_sent:
        await message.answer('Нет новых объявлений')
        return None
    db.insert_into_sent_messages(user_id, ad.ad_id)
    try:
        #log.info("_send_message SENDING MESSAGE")
        await message.answer_photo(ad.photo_url[0], caption=_format_message(ad), parse_mode=types.ParseMode.HTML)
    except BadRequest:
        await message.answer(f'{ad.ad_name}\nЦена: {ad.price}\nАдрес: {ad.address_title}\nСсылка: {ad.url}')

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    user_id, username = message.from_user.id, message.from_user.username
    start_buttons = ['Начать', 'Последнее 📢', 'Стоп']
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True) 
    keyboard.add(*start_buttons)
    if db.user_is_new(user_id):
        #log.info("INITIALIAZING NEW USER")
        db.init_new_user(user_id, username)
    await message.answer("Привет! Я буду уведомлять тебя о новых обявлениях на сайтах недвижимости\
\n\nНачать - получать все новые объявления как только они появляются на сайте\
\n\nПоследнее 📢 - получить последнее объявление\
\n\nСтоп - отключить уведомления."\
            , reply_markup=keyboard)

@dp.message_handler(Text(equals='Последнее 📢'))
async def send_newest_ad(message: types.Message):
    ad = db.fetch_one_from_db()
    await _send_message(message, ad)

async def _send_infinite_notifications(message: types.Message):
    user_id = message.from_user.id
    queue = db.update_queue(user_id)
    #log.info(f"MAIN NOTIFICATION LOOP QUEUE: {len(queue)}")
    while True:
        if not queue:
            queue = db.update_queue(user_id)
            await asyncio.sleep(5)
        else:
            ad_from_queue = queue.pop()
            await _send_message(message, ad_from_queue)
            await asyncio.sleep(5)

def _create_user_tasks(message: types.Message):
    # for some reason creating task also runs it thats why this function look wired
    user_id = message.from_user.id
    if user_id not in list(USERS_TASKS.keys()):
        task = asyncio.create_task(_send_infinite_notifications(message))
        USERS_TASKS.update({user_id: task})

@dp.message_handler(Text(equals=['Начать', 'Стоп']))
async def infinite_notifications(message: types.Message):
    user_id = message.from_user.id
    if message.text == 'Начать':
        #log.info("RECIEVED MESSAGE 'Начать'")
        _create_user_tasks(message)
    elif message.text == 'Стоп': 
        #log.info("RECIEVED MESSAGE 'Стоп'")
        if USERS_TASKS.get(user_id):
            task = USERS_TASKS.pop(user_id)
            task.cancel()

async def _retrive_data_from_scrapper(_type, rooms, rent_period):
    data = await krishakz_scrapper('arenda', 1, 2) 
    return data

async def update_database():
    #log.info('updating database')
    while True:
        houses_data = await _retrive_data_from_scrapper('arenda', 1, 2)
        db.insert_into_database(houses_data)
        await asyncio.sleep(random.randint(40, 60))

if __name__ == '__main__':
    #dp.loop.create_task(update_database())
    executor.start_polling(dp, skip_updates=True)

