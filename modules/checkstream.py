from aiohttp import client
import requests
from dotenv import load_dotenv
import os
import trio
import logging

client_id=os.environ.get("Client-ID-Twitch")

async def checkUser(userName, token): #returns true if online, false if not
    url = 'https://api.twitch.tv/helix/streams?user_login='+userName
    #url = url.rstrip()
    client_id=os.environ.get("Client-ID-Twitch")

    load_dotenv()

    API_HEADERS = {
        'Client-ID' : client_id,
        'Authorization' : 'Bearer ' + token,
    }

    try:
        #logging.printlog("🔎 checking user: "+userName)

        req = requests.get(url, headers=API_HEADERS)
        jsondata = req.json()

        if len(jsondata['data']) == 1:
            return True

        else:
            return False
            
    except Exception as e:
        logging.printlog("⁉️ Error checking user: ", e)
        return False