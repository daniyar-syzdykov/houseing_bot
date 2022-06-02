from krishakz_parser import krishakz_scrapper
import psycopg2
import json

#CONNECTION = sqlite3.connect('test.db')
#CURSOR = CONNECTION.cursor()

conn = psycopg2.connect()


def _save_data_to_database(data):
    conn = psycopg2.connect()

def _retrive_data_from_scrapper(_type, rooms, rent_period):
    data = krishakz_scrapper('arenda', 1, 2) 
    return data


def main():
    houses_data = _retrive_data_from_scrapper('arenda', 1, 2) 
    _save_data_to_database(houses_data)


if __name__ == '__main__':
    main()
