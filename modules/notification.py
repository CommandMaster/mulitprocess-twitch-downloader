import requests
from dotenv import load_dotenv
load_dotenv()
import os
import trio
from logbook import Logger, StreamHandler

Authtoken=os.environ.get("Authorization-IFTTT")
event=os.environ.get("event")
user=''

async def notification(message):
    log = Logger(user)
    report = {}
    report["value1"] = message
    requests.post(f"https://maker.ifttt.com/trigger/{event}/with/key/{Authtoken}", data=report)

    log.info(f'📨 send message:"{message}", to event:"{event}"')