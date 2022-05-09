import requests
from dotenv import load_dotenv
import modules.log as log
load_dotenv()
import os
import trio

Authtoken=os.environ.get("Authorization-IFTTT")
event=os.environ.get("event")

async def notification(message):
    report = {}
    report["value1"] = message
    requests.post(f"https://maker.ifttt.com/trigger/{event}/with/key/{Authtoken}", data=report)

    log.printlog('', f'📨 send message:"{message}", to event:"{event}"')