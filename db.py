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
file = open('houses.json', 'r')
raw_json = json.load(file)

#cur.execute("""INSERT INTO houses (ad_id, type, ad_name, price, address_title, country, 
#        region, city, street, house_num, rooms, owners_name, url, added_date) 
#        VALUES (222, 'arenda', 'dom na kamzian 33', 115000, 'lenina 23/4', 'kazakhstan',
#        '014', 'pavlodar', 'lenina', '23/4', 1, '888', 'krisha.kz/dom2',
#        '2016-06-22 19:10:25-07');""")

def create_db():
    pass

def create_tables(table_name, columns):
    cur.execute(f"CREATE TABLE {table_name.lower()} ({columns});")
    conn.commit()

def write_into_houses(rj):
    table = 'hoUses'
    for ad_id in rj:
        fields = 'ad_id, type, ad_name, price, address_title, country, region,\
city, street, house_num, rooms, owners_name, url, added_date' 
        values = [] 
        #print(raw_json[ad_id][0]['name'])
        values.append(ad_id)
        values.append(rj[ad_id][0]['type'])
        values.append(rj[ad_id][0]['ad_name'])
        values.append(rj[ad_id][0]['price'])
        values.append(rj[ad_id][0]['address_title'])
        values.append(rj[ad_id][0]['address']['country'])
        values.append(rj[ad_id][0]['address']['region'])
        values.append(rj[ad_id][0]['address']['city'])
        values.append(rj[ad_id][0]['address']['street'])
        values.append(rj[ad_id][0]['address']['house_num'])
        values.append(rj[ad_id][0]['rooms'])
        values.append(rj[ad_id][0]['owners_name'])
        values.append(rj[ad_id][0]['url'])
        values.append(rj[ad_id][0]['added_date'])

        write_into_tables(table, f"({fields})", tuple(values))

def construct_query(table, foreign_keys, child_tables, fields):
    pass

def write_into_tables(table, fields, values):
    cur.execute(f"INSERT INTO {table.lower()} {fields} VALUES {values}")
    conn.commit()


def read_from_db():
    cur.execute("""
        SELECT houses.*, ARRAY_AGG(photos.photo_url) as photos FROM houses
        LEFT JOIN photos ON houses.ad_id = photos.ad_id
        GROUP BY houses.ad_id ORDER BY houses.added_date DESC;""")
    return cur.fetchall()

write_into_houses(raw_json)

cur.close()
conn.close()
