import logging
import aiohttp
import asyncio


async def step_one_request(data):
    url = 'http://91.213.99.234:8000/api/request-step-one'
    payload = {
        "phone": int(data['phone']),
        "f_name": data['f_name'],
        "l_name": data['l_name'],
        "s_name": data['s_name'],
        "gender": data['gender'],
        "birthday": data['birthday'],
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            try:
                return await resp.json()
            except:
                return {'success': False}


async def step_two_request(data):
    url = 'http://91.213.99.234:8000/api/request-step-two'
    payload = {
        "phone": int(data['phone']),
        "farm_name": data['farm_name'],
        "farm_type": data['farm_type'],
        "position": data['position'],
        "district_id": data['district_id'],
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            try:
                return await resp.json()
            except:
                return {'success': False}



async def certificate_download(data):
    url = 'http://91.213.99.234:8000/api/request/certificate'
    payload = {
        "certificate_id": int(data),
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            try:
                return await resp.json()
            except:
                return {'success': False}


# async def get_regions():
#     async with aiohttp.ClientSession() as session:
#         async with session.get('https://aztester.uz/api-core/api/v1/region') as response:
#             return await response.json()

async def get_region_with_districts():
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://91.213.99.234:8000/api/region/with-district') as response:
            return await response.json()  