import json
import random 
import asyncio
import aiohttp
import datetime as dt
from bs4 import BeautifulSoup
import db

HEADERS = {
    'User-Agent': 'PostmanRuntime/7.29.0',
    'Accept': '*/*',
    'Connection': 'keep-alive',
}

async def _get_data_from_url(url, session):
    print(url)
    async with session.get(url=url, headers=HEADERS) as response:
        return await response.text()

def _parse_response(response, tag, args):
    #print('PARSER RESPONSE TEXT: ', response.text())
    soup = BeautifulSoup(response, 'lxml')
    raw_data = soup.find(tag, args)
    return raw_data

def _normalize_json(raw_text):
    text = raw_text.strip()
    normalized_json = json.loads(text[11:-1])
    return normalized_json 

def _get_ad_ids(json_data):
    ids = json_data['search']['ids']
    print(f'IDS: {ids}')
    return ids 

async def _get_single_ads_info(ids, _type, session):
    houses = {}
    for _id in ids:
        url = f'https://krisha.kz/a/show/{_id}'
        response = await _get_data_from_url(url, session)
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

async def scrape(ad_type: str, rooms: int, period:int, page: int, db_ad_ids: list) -> dict:
    async with aiohttp.ClientSession() as session:
        url = f'https://krisha.kz/{ad_type}/kvartiry/pavlodar/?das[live.rooms]={rooms}&das[rent.period]={period}&page=1&page={page}'
        queue = []
        response = await _get_data_from_url(url, session)
        raw_data = _parse_response(response, 'script', {'id': 'jsdata'})
        normalized_json = _normalize_json(raw_data.text)
        ad_ids = _get_ad_ids(normalized_json)
        for ad_id in ad_ids:
            if ad_id not in db_ad_ids:
                queue.append(ad_id)
        if not queue: print('no new ads')
        houses = await _get_single_ads_info(queue, ad_type, session)
        #with open('houses.json', 'w') as f:
        #    json.dump(houses, f, ensure_ascii=false)
        return houses

async def krishakz_scrapper(ad_type:str, rooms:int, period:int):
    db_ad_ids = db.fetch_all_from_db()
    db_ad_ids = [db_ad_ids[i].ad_id for i in range(len(db_ad_ids))]
    houses = {}
    if not db_ad_ids:
        for i in range(5, 0, -1):
            data = await scrape(ad_type, rooms, period, page=i, db_ad_ids=db_ad_ids)
            houses.update(data)
            print(len(houses))
            await asyncio.sleep(random.randint(40, 60))
        return houses
    houses = await scrape(ad_type, rooms, period, 1, db_ad_ids=db_ad_ids)
    return houses

if __name__ == '__main__':
    asyncio.run(krishakz_scrapper('arenda', 1, 2))

