import requests
import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '5509187287:AAE8EXqIEGsXCCzBJ-8GbnHeS49UGMRKVUQ'
URL = f'https://api.telegram.org/bot{API_TOKEN}/getMe'

logging.BasicConf(level=logging.INFO)
