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

async def get_region_with_districts():
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"http://91.213.99.234:8000/api/region/with-district"
        ) as response:
            return await response.json()

print(asyncio.run(check_phone('998998881965')))