import json
import random 
import time
import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
}
def get_data_from_url(url):
    response = requests.get(url=url, headers=HEADERS)
    return response

def parse_reponse(response, tag, args):
    soup = BeautifulSoup(response.text, 'lxml')
    raw_data = soup.find_all(tag, args)
    return raw_data


def normalize_data(raw_data):
    pass

def get_list_of_all_ads(url):
    response = get_data_from_url(url)
    data = parse_reponse(response, 'div', {'data-cy': 'l-card'})
    return data

def get_single_ads_info(ads):
    pass

def olx_parser():
    url = 'https://www.olx.kz/d/nedvizhimost/kvartiry/arenda-dolgosrochnaya/pavlodar/?search%5Bfilter_float_number_of_rooms:from%5D=1&search%5Bfilter_float_number_of_rooms:to%5D=1'
    response = get_data_from_url(url)
    raw_data = parse_response(response)
def main():
    olx_parser()


if __name__ == '__main__':
    main()
