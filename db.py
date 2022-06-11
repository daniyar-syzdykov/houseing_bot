import sys
import os
import json
import psycopg2
import psycopg2.errorcodes
from collections import namedtuple
from typing import NamedTuple
from dataclasses import dataclass

#    await message.reply(f'{ad.db_id} {ad.ad_id} {ad.ad_type} {ad.ad_name}\
#{ad.price} {ad.address_title} {ad.country} {ad.region} {ad.city} {ad.street}\
#{ad.house_num} {ad.rooms} {ad.owners_name} {ad.url} {ad.added_date} {ad.photo_url}')

class DataFromDB(NamedTuple):
    db_id: int
    ad_id: int
    ad_type: str
    ad_name: str
    price: int
    address_title: str
    country: str
    region: str
    city: str
    street: str
    house_num: str
    rooms: int
    owners_name: str
    url: str
    added_date: list
    photo_url: list[str]


conn = psycopg2.connect(
        host='localhost',
        dbname='psql_test',
        user='postgres',
        password='postgres'
    )
cur = conn.cursor()


class SqlQuerys:
    get_all_ad_ids = "SELECT houses.ad_id FROM houses;"
    get_all_map_data = "SELECT map_data.ad_id FROM map_data;"
    get_all_photo_urls ="SELECT photos.photo_url FROM photos;" 

def _init_database():
    #print('initializing database')
    with open('createdb.sql', 'r') as f:
        sql = f.read()
    cur.execute(sql)
    conn.commit()

def _write_into_houses(raw_json):
    table_name = 'houses'
    cur.execute(SqlQuerys.get_all_ad_ids)
    db_ad_ids = cur.fetchall()
    fields = 'ad_id, type, ad_name, price, address_title, country, region,\
city, street, house_num, rooms, owners_name, url, added_date' 
    for ad_id in raw_json:
        if (ad_id, ) in db_ad_ids:
            continue
        values = [] 
        values.append(ad_id)
        values.append(raw_json[ad_id][0]['type'])
        values.append(raw_json[ad_id][0]['ad_name'])
        values.append(raw_json[ad_id][0]['price'])
        values.append(raw_json[ad_id][0]['address_title'])
        values.append(raw_json[ad_id][0]['address']['country'])
        values.append(raw_json[ad_id][0]['address']['region'])
        values.append(raw_json[ad_id][0]['address']['city'])
        values.append(raw_json[ad_id][0]['address']['street'])
        values.append(raw_json[ad_id][0]['address']['house_num'])
        values.append(raw_json[ad_id][0]['rooms'])
        values.append(raw_json[ad_id][0]['owners_name'])
        values.append(raw_json[ad_id][0]['url'])
        values.append(raw_json[ad_id][0]['added_date'])
        _write_into_table(table_name, f"({fields})", tuple(values))

def init_new_user(user_id, username):
    table_name = 'sent_messages'
    fields = 'user_id, ad_id, username'
    values = [user_id, 0, username]
    _write_into_table(table_name, f"({fields})", tuple(values))

def insert_into_sent_messages(user_id, ad_id, username):
    table_name = 'sent_messages'
    fields = 'user_id, ad_id, username'
    values = [user_id, ad_id, username]
    _write_into_table(table_name, f"({fields})", tuple(values))
    
def _write_into_photos(raw_json):
    table_name = 'photos'
    fields = 'ad_id, photo_url'
    cur.execute(SqlQuerys.get_all_photo_urls)
    photo_urls = cur.fetchall()
    for ad_id in raw_json:
        for photo in raw_json[ad_id][0]['photo']:
            print((photo['src'], ))
            if (photo['src'], ) not in photo_urls:
                values = []
                values.append(ad_id)
                values.append(photo['src'])
                _write_into_table(table_name, f"({fields})", tuple(values))

def _write_into_maps(raw_json):
    table_name = 'map_data'
    fields = 'ad_id, lat, lon, zoom'
    cur.execute(SqlQuerys.get_all_ad_ids)
    db_ad_ids = cur.fetchall()
    for ad_id in raw_json:
        if (ad_id, ) in db_ad_ids:
            continue
        values = []
        raw_json[ad_id][0]['map']
        values.append(ad_id)
        values.append(raw_json[ad_id][0]['map']['lat'])
        values.append(raw_json[ad_id][0]['map']['lon'])
        values.append(raw_json[ad_id][0]['map']['zoom'])
        _write_into_table(table_name, f"({fields})", tuple(values))

def _convert_sql_to_named_tuple(data: tuple) -> DataFromDB:
    d = data
    return DataFromDB(
        db_id=d[0], ad_id=d[1], ad_type=d[2], ad_name=d[3], price=d[4],\
        address_title=d[5], country=d[6], region=d[7], city=d[8], street=d[9],\
        house_num=d[10], rooms=d[11], owners_name=d[12], url=d[13],\
        added_date=d[14], photo_url=d[15])


    
def _write_into_table(table, fields, values):
    print(f"INSERT INTO {table.lower()} {fields} VALUES {values}")
    cur.execute(f"INSERT INTO  {table.lower()} {fields} VALUES {values}")
    conn.commit()

def fetch_all_from_db() -> list[DataFromDB]:
    cur.execute("""
    SELECT houses.*, ARRAY_AGG(photos.photo_url) as photos FROM houses
    LEFT JOIN photos ON houses.ad_id = photos.ad_id
    GROUP BY houses.ad_id ORDER BY houses.added_date DESC;""")
    data = cur.fetchall()
    result = []
    for house in data:
        result.append(_convert_sql_to_named_tuple(house))
    return result

def fetch_last_n_from_db(*n) -> list[DataFromDB]:
    cur.execute("""
    SELECT houses.*, ARRAY_AGG(photos.photo_url) as photos FROM houses
    LEFT JOIN photos ON houses.ad_id = photos.ad_id
    GROUP BY houses.ad_id ORDER BY houses.added_date DESC;""")
    data = cur.fetchmany(n)
    result = []
    for house in data:
        result.append(_convert_sql_to_named_tuple(house))
    return result

def fetch_one_from_db() -> DataFromDB:
    cur.execute("""
    SELECT houses.*, ARRAY_AGG(photos.photo_url) as photos FROM houses
    LEFT JOIN photos ON houses.ad_id = photos.ad_id
    GROUP BY houses.ad_id ORDER BY houses.added_date DESC;""")
    data = cur.fetchone()
    result = _convert_sql_to_named_tuple(data)
    return result

def read_from_map_data() -> list[DataFromDB]:
    cur.execute("SELECT * FROM map_data;")
    data = cur.fetchall()
    result = []
    for m in data:
        result.append(_convert_sql_to_named_tuple(m))
    return result

def insert_into_database(raw_json):
    try:
        _write_into_houses(raw_json)
        _write_into_maps(raw_json)
        _write_into_photos(raw_json)
    except psycopg2.Error as err:
        conn.rollback()
        print('!ERROR: ', err)
        if err.pgcode == psycopg2.errorcodes.FOREIGN_KEY_VIOLATION:
            conn.rollback()


_init_database()
if __name__ == '__main__':
    #fetch_one_from_db()
    pass
