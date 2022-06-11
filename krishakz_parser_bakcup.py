import json
import random 
import asyncio
import datetime as dt
import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'PostmanRuntime/7.29.0',
    'Accept': '*/*',
    'Connection': 'keep-alive',
}

def _get_data_from_url(url):
    print(url)
    response = requests.get(url=url, headers=HEADERS)
    print(response.status_code)
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

async def _get_single_ads_info(ids, _type):
    houses = {}
    for _id in ids:
        url = f'https://krisha.kz/a/show/{_id}'
        response = _get_data_from_url(url)
        raw_json = _parse_response(response, 'script', {'id': 'jsdata'})
        data = _normalize_json(raw_json.text) 
        ads_info = {}
        ads_info['type'] = _type
        ads_info['ad_name'] = data['advert']['title']
        ads_info['price'] = data['advert']['price']
        ads_info['photo'] = data['advert']['photos']
        ads_info['address_title'] = data['advert']['addressTitle']
        ads_info['address'] = data['advert']['address']
        ads_info['map'] = data['advert']['map']
        ads_info['rooms'] = data['advert']['rooms']
        ads_info['owners_name'] = data['advert']['ownerName']
        ads_info['url'] = url 
        ads_info['added_date'] = str(dt.datetime.now() + dt.timedelta(hours=6)) 
        houses[_id] = [ads_info]
        await asyncio.sleep(random.randint(3, 6))
    return houses

async def krishakz_scrapper(ad_type:str, rooms:int, period:int):
    url = f'https://krisha.kz/{ad_type}/kvartiry/pavlodar/?das[live.rooms]={rooms}&das[rent.period]={period}'
    response = _get_data_from_url(url)
    raw_data = _parse_response(response, 'script', {'id': 'jsdata'})
    normalized_json = _normalize_json(raw_data.text)
    ads_ids = _get_ad_ids(normalized_json)
    houses = asyncio.run(_get_single_ads_info(ads_ids, ad_type))
    with open('houses.json', 'w') as f:
        json.dump(houses, f, ensure_ascii=False)
    return houses

async def main():
    await krishakz_scrapper('arenda', 1, 2) 


if __name__ == '__main__':
    asyncio.run(main())

