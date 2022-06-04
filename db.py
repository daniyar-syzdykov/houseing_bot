import psycopg2
import sys
import os
import json

conn = psycopg2.connect(
        host='localhost',
        dbname='psql_test',
        user='test_user',
        password='testpass123'
    )
cur = conn.cursor()

def _init_database():
    print('initializing database')
    with open('createdb.sql', 'r') as f:
        sql = f.read()
    cur.execute(sql)
    conn.commit()

def write_into_houses(raw_json):
    table = 'houses'
    for ad_id in raw_json:
        fields = 'ad_id, type, ad_name, price, address_title, country, region,\
city, street, house_num, rooms, owners_name, url, added_date' 
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
        try:
            _write_into_table(table, f"({fields})", tuple(values))
        except psycopg2.errors.UniqueViolation as err:
            print(err)
    
def write_into_photos(raw_json):
    table_name = 'photos'
    fields = 'ad_id, photo_url'
    for ad_id in raw_json:
        for photo in raw_json[ad_id][0]['photo']:
            values = []
            values.append(ad_id)
            values.append(photo['src'])
            _write_into_table(table_name, f"({fields})", tuple(values))

def write_into_maps(raw_json):
    table_name = 'map_data'
    fields = 'ad_id, lat, lon, zoom'
    for ad_id in raw_json:
        values = []
        raw_json[ad_id][0]['map']
        values.append(ad_id)
        values.append(raw_json[ad_id][0]['map']['lat'])
        values.append(raw_json[ad_id][0]['map']['lon'])
        values.append(raw_json[ad_id][0]['map']['zoom'])
        _write_into_table(table_name, f"({fields})", tuple(values))

def read_from_db():
    cur.execute("""
        SELECT houses.*, ARRAY_AGG(photos.photo_url) as photos FROM houses
        LEFT JOIN photos ON houses.ad_id = photos.ad_id
        GROUP BY houses.ad_id ORDER BY houses.added_date DESC;""")
    return cur.fetchall()

def _write_into_table(table, fields, values):
    print(f"INSERT INTO {table.lower()} {fields} VALUES {values}")
    cur.execute(f"INSERT INTO  {table.lower()} {fields} VALUES {values}")
    conn.commit()

_init_database()
if __name__ == '__main__':
    _init_database()
