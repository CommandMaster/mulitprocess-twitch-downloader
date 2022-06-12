import json
from aiohttp import client
import requests
import time
import dotenv
import modules.notification as notification
from logbook import Logger, StreamHandler
import trio
import os

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
clientid = os.environ.get("Client-ID-Twitch")
clientsecret = os.environ.get("Authorization-Twitch")

async def post(user):
    log = Logger(user)
    daysec = 2456000
    url = 'https://id.twitch.tv/oauth2/token?client_id='+clientid+'&client_secret='+clientsecret+'&grant_type=client_credentials'
    req = requests.post(url)
    jsondata = req.json()
    token = jsondata['access_token']
    wait = jsondata['expires_in']-daysec

    log.info('🔑 getting token')
    #log.info(jsondata)
    log.info('🔑 auth token is= '+token)
    days = wait%60%60
    log.info('💤 sleeps for '+str(wait)+'s or '+str(days))

    wait = wait + time.time()
    
    await notification.notification('new token generated in '+user+' for'+str(days)+'days! ' + token)

    return wait, token

