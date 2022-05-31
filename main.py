from krishakz_parser import krishakz_scrapper
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base
from sqlalchemy import text, MetaData
import json

#CONNECTION = sqlite3.connect('test.db')
#CURSOR = CONNECTION.cursor()

ENGINE = create_engine('sqlite:///sqlite_test.db', echo=True, future=True)
meta = MetaData()

photos = Table(
        'photos', meta,
        Column('id', Integer, primary_key=True),
        Column('src', String),
        Column('ad_id', Integer, ForeignKey=True),
        )

map = Table(
        'photos', meta,
        Column('id', Integer, primary_key=True),
        Column('src', String),
        Column('ad_id', Integer, ForeignKey=True),
        )
#with engine.begin() as conn:
   #conn.execute(text("CREATE TABLE test_table (x int, y int)"))
   # conn.execute(
   #     text("INSERT INTO test_table (x, y) VALUES (:x, :y)"),
   #     [{'x': 1, 'y': 1}, {'x': 2, 'y': 4}]
   #     )
   #result = conn.execute(text("SELECT x, y FROM test_table"))
   # for row in result:
   #     print(f'x: {row.x} y: {row.y}')
   #print(result.all())


def _create_tables_in_db():
    pass

def _save_data_in_tables(data):
    with ENGINE.begin() as conn:
        conn.execute()

def _retrive_data_from_scrapper(rooms, rent_period):
    json_file = open('houses.json', 'r')
    data = json.load(json_file)
    return data


def main():
    houses_data = _retrive_data_from_scrapper(1, 2) 
    _save_data_in_tables(houses_data)


if __name__ == '__main__':
    main()
