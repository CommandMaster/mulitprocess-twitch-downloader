from aiohttp import client
import requests
from dotenv import load_dotenv
from rich import print
import os
import trio

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
        #print("🔎 checking user: "+userName)

        req = requests.get(url, headers=API_HEADERS)
        jsondata = req.json()

        if len(jsondata['data']) == 1:
            return True

        else:
            return False
            
    except Exception as e:
        print("⁉️ Error checking user: ", e)
        return False