from __future__ import unicode_literals
from dotenv import load_dotenv
load_dotenv()
from datetime import date
#from rich import print
import checkstream
import dl_stream
import getauth
import os
import sys
import time
import trio

listname = os.environ.get("LISTNAME")
channellist = open(listname, "r")
Lines = channellist.readlines()
dir = os.environ.get("DIR")
#os.chdir(dir)

print("📂 save path is: "+dir)

#folder routine2
async def sub1(channel):
    global workdir
    today = date.today()
    folder = channel + "-stream-" + str(today)

    if os.path.isdir(workdir+'/'+folder) == False:
        os.mkdir(workdir+'/'+folder)
        print("📂 sub folder created for: "+channel)
    else:
        print("📂 sub folder allready created for: "+channel)

    workdir = workdir+'/'+folder+'/'

    print("📂 working dir is: "+workdir)
    print("🔽 starting download")
    await dl_stream.dlstream(channel, folder, workdir)

#folder routine1
async def sub0(channel):
    global workdir
    #check ob save directoy online ist 
    workdir = dir+'/'+channel

    if os.path.isdir(dir+'/'+channel) ==False:
        os.mkdir(dir+'/'+channel)
        print("📂 folder created for: "+channel)
    else:
        print("📂 folder allready created for: "+channel)

    await sub1(channel)

async def starup(channel):
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
            print("🔴 channel: "+channel+" is online")
            await sub0(channel)
        else:
            #print("⚫ channel: "+channel+" is offline")
            await trio.sleep(600)


async def main():
    print("🧑‍🤝‍🧑 starting threads")

    async with trio.open_nursery() as nursery:
        for line in Lines:
            if line == '' or '':
                pass
            else:
            	nursery.start_soon(starup, line.rstrip())

trio.run(main)
