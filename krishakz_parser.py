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

def _get_data_from_url(url):
    response = requests.get(url=url, headers=HEADERS)
    return response

def _parse_response(response, tag, args):
    soup = BeautifulSoup(response.text, 'lxml')
    raw_data = soup.find(tag, args)
    return raw_data

def _normalize_json(raw_text):
    text = raw_text.strip()
    normalized_json = json.loads(text[11:-1])
    return normalized_json 

def _get_ad_ids(json_data):
    ids = json_data['search']['ids']
    return ids 

def _get_single_ads_info(ids):
    houses = {}
    for _id in ids:
        url = f'https://krisha.kz/a/show/{_id}'
        response = _get_data_from_url(url)
        raw_json = _parse_response(response, 'script', {'id': 'jsdata'})
        data = _normalize_json(raw_json.text) 
        ads_info = {}
        ads_info['name'] = data['advert']['title']
        ads_info['price'] = data['advert']['price']
        ads_info['photo'] = data['advert']['photos']
        ads_info['address_title'] = data['advert']['addressTitle']
        ads_info['address'] = data['advert']['address']
        ads_info['map'] = data['advert']['map']
        ads_info['rooms'] = data['advert']['rooms']
        ads_info['owners_name'] = data['advert']['ownerName']
        ads_info['url'] = url 
        houses[_id] = [ads_info]
        time.sleep(random.randint(3, 6))
    return houses

def krishakz_scrapper(rooms:int, period:int):
    url = f'https://krisha.kz/arenda/kvartiry/pavlodar/?das[live.rooms]={rooms}&das[rent.period]={period}'
    response = _get_data_from_url(url)
    raw_data = _parse_response(response, 'script', {'id': 'jsdata'})
    normalized_json = _normalize_json(raw_data.text)
    ads_ids = _get_ad_ids(normalized_json)
    houses = _get_single_ads_info(ads_ids)
    with open('houses.json', 'w') as f:
        json.dump(houses, f, ensure_ascii=False)
    return houses

def main():
    krishakz_scrapper(1, 2) 


if __name__ == '__main__':
    main()

