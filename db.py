import sys
import os
import json
import psycopg2
import psycopg2.errorcodes

conn = psycopg2.connect(
        host='localhost',
        dbname='psql_test',
        user='test_user',
        password='testpass123'
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
        _write_into_table(table_name, f"({fields})", tuple(values))
    
def _write_into_photos(raw_json):
    table_name = 'photos'
    fields = 'ad_id, photo_url'
    for ad_id in raw_json:
        for photo in raw_json[ad_id][0]['photo']:
            values = []
            values.append(ad_id)
            values.append(photo['src'])
            _write_into_table(table_name, f"({fields})", tuple(values))

def _write_into_maps(raw_json):
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

def read_last_n_from_db(n):
    return cur.fetchall()[:n]

def read_last_data_from_database():
    return cur.fetchone()

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
    pass
