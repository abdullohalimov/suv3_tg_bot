FROM python:3.10-slim

WORKDIR /usr/src/app/sms

COPY requirements.txt /usr/src/app/sms
RUN pip install -r /usr/src/app/sms/requirements.txt
COPY . /usr/src/app/sms

CMD [ "uvicorn", "send_sms_api:app"]