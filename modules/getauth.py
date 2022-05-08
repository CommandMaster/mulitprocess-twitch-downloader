import json
from aiohttp import client
import requests
import time
import dotenv
import modules.notification as notification
import modules.log as log
import trio
import os

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
clientid = os.environ.get("Client-ID-Twitch")
clientsecret = os.environ.get("Authorization-Twitch")

async def post(user):
    daysec = 2456000
    url = 'https://id.twitch.tv/oauth2/token?client_id='+clientid+'&client_secret='+clientsecret+'&grant_type=client_credentials'
    req = requests.post(url)
    jsondata = req.json()
    token = jsondata['access_token']
    wait = jsondata['expires_in']-daysec

    log.printlog('🔑 getting token, of: '+user)
    #log.printlog(jsondata)
    log.printlog('🔑 auth token is= '+token+', of: '+user)
    days = wait%60%60
    log.printlog('💤 sleeps for '+str(wait)+'s or '+str(days)+'d, of: '+user)

    wait = wait + time.time()
    
    await notification.notification('new token generated in '+user+' for'+str(days)+'days! ' + token)

    return wait, token

