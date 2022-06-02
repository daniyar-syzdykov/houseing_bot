import psycopg2
import sys
import os


conn = psycopg2.connect(
        host='localhost',
        dbname='psql_test',
        user='test_user',
        password='testpass123'
    )

cur = conn.cursor()
t = 'houses'
f = 'houses.*'
v = ('maps', 'photos')

def save_into_db(raw_json, table, fields, values):
    print(f"INSERT INTO {table} {fields} VALUES {values}")
    cur.execute(f"INSERT INTO {table} {fields} VALUES {values}")
    conn.commit()
    cur.close()
    conn.close()

def read_from_db(raw_json, table, fields, child_tables):
    return f"SELECT {fields}, ARRAY_AGG(photos.photo_url) as photos FROM {table} LEFT JOIN {child_tables[0]} ON {table}.ad_id = {child_tables[0]}.ad_id\
 LEFT JOIN {child_tables[1]} ON {table}.ad_id = {child_tables[1]}.ad_id GROUP BY {table}.ad_id, {child_tables[0]}.*;"
ans = read_from_db(1, t, f, v)

