import json
import db
import bot
import asyncio
import psycopg2
from krishakz_parser import krishakz_scrapper


def _read_from_database():
    db.fetch_all_from_db()
    
   
def _save_data_to_database(data):
    print("save_to_database")
    db.insert_into_database(data)

def _retrive_data_from_scrapper(_type, rooms, rent_period):
    data = krishakz_scrapper('arenda', 1, 2) 
    return data

async def main():
    houses_data = await _retrive_data_from_scrapper('arenda', 1, 2)
    #file = open('houses.json', 'r')
    #houses_data = json.load(file)
    _save_data_to_database(houses_data)

if __name__ == '__main__':
    asyncio.run(main())

