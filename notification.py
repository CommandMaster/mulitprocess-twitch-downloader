import requests
from rich import print
from dotenv import load_dotenv
load_dotenv()
import os
import trio

Authtoken=os.environ.get("Authorization-IFTTT")
event=os.environ.get("event")

async def notification(message):
    report = {}
    report["value1"] = message
    requests.post(f"https://maker.ifttt.com/trigger/{event}/with/key/{Authtoken}", data=report)

    print(f'📨 send message:"{message}", to event:"{event}"')