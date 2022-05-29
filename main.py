import scrappers
from krishakz_parser import krishakz_scrapper
import psycopg2
from config import host, user, password, db_name
import sqlite3

def _create_tables_in_db():
    connection = sqlite3.connect('test.db') 
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE houses(adress text, price integer)""") 
    connection.commit()
    connection.close()
def _save_data_in_tables():
    pass

def _retirive_data_from_scrapper(rooms, rent_period):
    krishakz_data = krishakz_scrapper(rooms, rent_period)
    data = krishakz_data


def main():
    _create_tables_in_db()


if __name__ == '__main__':
    main()
