from __future__ import unicode_literals
from xml.etree.ElementInclude import include
from dotenv import load_dotenv
load_dotenv()
from datetime import date
import modules.checkstream as checkstream
import modules.dl_stream as dl_stream
import modules.getauth as getauth
import modules.weighting as weighting
import modules.notification as notification
import logbook
import sys
import os
import datetime
import time
import trio

logbook.StreamHandler(sys.stdout).push_application()
log = logbook.Logger('main')
logbook.set_datetime_format("local")

now = datetime.datetime.now()
listname = os.environ.get("LISTNAME")
channellist = open(listname, "r")
Lines = channellist.readlines()
dir = os.environ.get("DIR")

log.info("📂 save path is: "+dir)

#folder routine2
async def sub1(channel):
    workdir = dir+'/'+channel
    today = date.today()
    folder = channel + "-stream-" + str(today)

    if os.path.isdir(workdir+'/'+folder) == False:
        os.mkdir(workdir+'/'+folder)
        log.info("📂 sub folder created")
    else:
        log.info("📂 sub folder allready created")

    workdir = workdir+'/'+folder+'/'

    log.info("📂 working dir is: "+workdir)
    log.info("⬇️ starting download")
    filename = now.strftime("%H.%M")
    await dl_stream.dlstream(channel, filename, workdir)

#folder routine1
async def check_main_folder(channel):

    if os.path.isdir(dir+'/'+channel) ==False:
        os.mkdir(dir+'/'+channel)
        log.info("📂 folder created")
    else:
        log.info("📂 folder allready created")

async def starup(channel):
    global log
    notification.user = channel
    await check_main_folder(channel)
    await weighting.readstate(channel)
    
    while True:
        log = logbook.Logger(channel)
        #check if token is to old
        try:
            if wait <= time.time():
                wait, token = await getauth.post(channel)
        except:
            wait = time.time()
            wait, token = await getauth.post(channel)
        
        #check streamstate
        if await checkstream.checkUser(channel, token) == True:
            log.info("🔴 is online")
            await weighting.onlinetimeweighting(channel)
            await sub1(channel)
        else:
            #log.info("⚫ channel: "+channel+" is offline")
            weights = await weighting.analyseweights()
            if weights == 'array error':
                log.error(weights)
                pass
            for hour in weights:
                if hour == now.hour:
                    #log.info("🕚 sleep for a minute")
                    await trio.sleep(60)
                else:
                    #log.info("🕚 sleep for 10 minute")
                    await trio.sleep(600)


async def starr_threads():
    log.info("🧑‍🤝‍🧑 starting threads")

    async with trio.open_nursery() as nursery:
        for line in Lines:
            if not line.rstrip():
                pass
            else:
            	nursery.start_soon(starup, line.rstrip())

if __name__ == "__main__":
    trio.run(starr_threads)