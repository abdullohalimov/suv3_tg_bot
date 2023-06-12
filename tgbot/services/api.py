import json
import logging
import aiohttp
import asyncio


async def step_one_request(data, chat_id):
    url = "http://91.213.99.234:8000/api/request-step-one"
    payload = {
        "birthday": data["birthday"],
        "device_type": 'bot',
        "district_id": data["district_id"],
        # "region_id": data["district_id"],
        "full_name": data["full_name"],
        "gender": data["gender"],
        "phone": int(data["phone"]),
        "chat_id": int(chat_id),

    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            try:
                return await resp.json()
            except:
                return {"success": False}

async def step_two_request(data):
    url = "http://91.213.99.234:8000/api/request-step-two"
    payload = {
        "phone": int(data["phone"]),
        "farm_name": data["farm_name"],
        "farm_type": data["farm_type"],
        "position": data["position"],
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            try:
                return await resp.json()
            except:
                return {"success": False}

async def certificate_download(data):
    url = "http://91.213.99.234:8000/api/request/certificate"
    payload = {
        "certificate_id": f"{data}",
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            if resp.content_type == "application/pdf":
                return await resp.read()
            elif resp.content_type == "text/html":
                return False
                return await resp.text()
                print(False)

async def check_phone(phone):
    payload = {
        "phone": int(phone),
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(f'http://91.213.99.234:8000/api/check-phone', data=payload) as resp:
            try:
                return await resp.json()
            except:
                return {"success": False}
            # logging.error(await resp.json())
            # # return resp

async def get_region_with_districts(lang):
    if lang in ['uz', 'ru']:
        header = {
            'Language': 'uz_cyrl',
        }
    else:
        header = {
        }
    async with aiohttp.ClientSession(headers=header) as session:
        async with session.get(
            f"http://91.213.99.234:8000/api/region/with-district"
        ) as response:
            return await response.json()

async def get_user_data_from_cert_id(cert_id):
    
    url = f'http://91.213.99.234:8000/api/request/{cert_id}'
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def send_feedback(data):
    url = 'http://91.213.99.234:8000/api/feedback'

    headers = {
        'accept': 'application/json', 
        'Content-Type': 'application/json'
    }

    rates: list = []

    for question in [[1, data['first']], [2, data['second']], [3, data['third']], [4, data['four']], [5, data['five']]]:
        rates.append({
            "question": f"{question[0]}",
            "rate": f"{question[1]}"
        })
    payload = {
        "rates": rates,
        "comment": f"{data['six']}", 
        "request_id": data['certificate_id']
    }
    # for i in range(0, len(rates)):
    #     payload[f'rates[{i}]'] = rates[i]
    print(payload)
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url, data=json.dumps(payload)) as response:
            # return await response.json()
            print(await response.text())
        
async def get_all_feedbacks():
    url = 'http://91.213.99.234:8000/api/feedback'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# print(asyncio.run(get_all_feedbacks()))

