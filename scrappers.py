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

def parse_response(response, tag, args):
    soup = BeautifulSoup(response.text, 'lxml')
    raw_data = soup.find(tag, args)
    return raw_data

def normalize_json(raw_text):
    text = raw_text.strip()
    normalized_json = json.loads(text[11:-1])
    return normalized_json 

def get_ad_ids(json_data):
    ids = list(json_data['data'].keys())
    return ids 

def get_single_ads_info(ids):
    ads_info = {}
    for _id in ids:
        url = 'https://krisha.kz/a/show/{_id}'
        response = get_data_from_url(url)
        raw_json = parse_response(response, 'script', {'id': 'jsdata'})
        data = normalize_json(raw_json)
        ads_info['name'] = data['advert']['title']
        ads_info['price'] = data['advert']['price']
        ads_info['photo'] = data['advert']['photos'][0]['src']
        ads_info['address_title'] = data['advert']['addressTitle']
        ads_info['address'] = data['advert']['address']
        ads_info['map'] = data['advert']['map']
        ads_info['rooms'] = data['advert']['rooms']
        ads_info['owners_name'] = data['advert']['ownersName']
        print(ads_info)
        time.sleep(random.randint(3, 6))
    return ads_info

def krishakz_scrapper(rooms:int, period:int):
    url = 'https://krisha.kz/arenda/kvartiry/pavlodar/?das[live.rooms]={rooms}&das[rent.period]={period}'
    response = get_data_from_url(url)
    raw_data = parse_response(response, 'script', {'id': 'jsdata'})
    normalized_json = normalize_json(raw_data)
    ads_ids = get_ad_ids(normalized_json)
    houses = get_single_ads_info(ads_ids)
    return houses

def main():
    krishakz_scrapper(1, 2) 


if __name__ == '__main__':
    main()






