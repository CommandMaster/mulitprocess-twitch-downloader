from __future__ import unicode_literals
from xml.etree.ElementInclude import include
from dotenv import load_dotenv
load_dotenv()
from datetime import date
import modules.checkstream as checkstream
import modules.dl_stream as dl_stream
import modules.getauth as getauth
import modules.weighting as weighting
import modules.log as log
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

log.printlog('',"📂 save path is: "+dir)

#folder routine2
async def sub1():
    global workdir, channel
    today = date.today()
    folder = channel + "-stream-" + str(today)

    if os.path.isdir(workdir+'/'+folder) == False:
        os.mkdir(workdir+'/'+folder)
        log.printlog(channel, "📂 sub folder created")
    else:
        log.printlog(channel, "📂 sub folder allready created")

    workdir = workdir+'/'+folder+'/'

    log.printlog(channel, "📂 working dir is: "+workdir)
    log.printlog(channel, "⬇️ starting download")
    await dl_stream.dlstream(channel, folder, workdir)

#folder routine1
async def sub0():
    global workdir, channel
    #check ob save directoy online ist 
    workdir = dir+'/'+channel

    if os.path.isdir(dir+'/'+channel) ==False:
        os.mkdir(dir+'/'+channel)
        log.printlog(channel, "📂 folder created")
    else:
        log.printlog(channel, "📂 folder allready created")

    await sub1()

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
            log.printlog(channel,  "🔴 is online")
            await weighting.onlinetimeweighting(channel)
            await sub0()
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
    log.printlog('',"🧑‍🤝‍🧑 starting threads")

    async with trio.open_nursery() as nursery:
        for line in Lines:
            if not line.rstrip():
                pass
            else:
            	nursery.start_soon(starup, line.rstrip())

trio.run(main)
