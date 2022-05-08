from __future__ import unicode_literals
from xml.etree.ElementInclude import include
from dotenv import load_dotenv
load_dotenv()
from datetime import date
import checkstream
import dl_stream
import getauth
import weighting
import log
import os
import datetime
import time
import trio

now = datetime.datetime.now()
listname = os.environ.get("LISTNAME")
channellist = open(listname, "r")
Lines = channellist.readlines()
dir = os.environ.get("DIR")
#os.chdir(dir)

log.printlog("📂 save path is: "+dir)

#folder routine2
async def sub1(channel):
    global workdir
    today = date.today()
    folder = channel + "-stream-" + str(today)

    if os.path.isdir(workdir+'/'+folder) == False:
        os.mkdir(workdir+'/'+folder)
        log.printlog("📂 sub folder created for: "+channel)
    else:
        log.printlog("📂 sub folder allready created for: "+channel)

    workdir = workdir+'/'+folder+'/'

    log.printlog("📂 working dir is: "+workdir)
    log.printlog("⬇️ starting download")
    await dl_stream.dlstream(channel, folder, workdir)

#folder routine1
async def sub0(channel):
    global workdir
    #check ob save directoy online ist 
    workdir = dir+'/'+channel

    if os.path.isdir(dir+'/'+channel) ==False:
        os.mkdir(dir+'/'+channel)
        log.printlog("📂 folder created for: "+channel)
    else:
        log.printlog("📂 folder allready created for: "+channel)

    await sub1(channel)

async def starup(channel):

    await weighting.readstate(channel)

    while True:
        #check if token is to old
        try:
            if wait <= time.time():
                wait, token = await getauth.post(channel)
        except:
            wait = time.time()
            wait, token = await getauth.post(channel)
        
        #check streamstate
        if await checkstream.checkUser(channel, token) == True:
            log.printlog("🔴 channel: "+channel+" is online")
            await weighting.onlinetimeweighting(channel)
            await sub0(channel)
        else:
            #log.printlog("⚫ channel: "+channel+" is offline")
            weights = await weighting.analyseweights()
            for hour in weights:
                if hour == now.hour:
                    #log.printlog("🕚 sleep for a minute")
                    await trio.sleep(60)
                else:
                    #log.printlog("🕚 sleep for 10 minute")
                    await trio.sleep(600)


async def main():
    log.printlog("🧑‍🤝‍🧑 starting threads")

    async with trio.open_nursery() as nursery:
        for line in Lines:
            if not line.rstrip():
                pass
            else:
            	nursery.start_soon(starup, line.rstrip())

trio.run(main)
