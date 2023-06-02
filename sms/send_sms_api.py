from typing import Annotated
from eskiz_sms import EskizSMS
from fastapi import FastAPI, Form

app = FastAPI()

async def send(phone, text):
    eskiz = EskizSMS('onlayn5588@gmail.com', 'v7hvvQMHqgsp2jED6g5MSvi38uRaeHfaOq618Fx7')
    try:
        return eskiz.send_sms(mobile_phone=f'{phone}', message=f'{text}')

    except:
        return {'success': False}
     


@app.post('/send_message')
async def send_message(phone: Annotated[str, Form()], message: Annotated[str, Form()]):
    return await send(phone=phone, text=message)

@app.post('/send_message_2/{phone}/{message}')
async def send_message(phone, message):
    return await send(phone=phone, text=message.replace('_', ' '))

@app.post('/send_message_3')
async def send_message(phone: int, message: str):
    return await send(phone=phone, text=message)