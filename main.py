from __future__ import unicode_literals
from xml.etree.ElementInclude import include
from dotenv import load_dotenv
load_dotenv()
from datetime import date
import checkstream
import dl_stream
import getauth
import os
import datetime
import time
import trio
import ast

listname = os.environ.get("LISTNAME")
channellist = open(listname, "r")
Lines = channellist.readlines()
dir = os.environ.get("DIR")
#os.chdir(dir)

print("📂 save path is: "+dir)

now = datetime.datetime.now()

#hour weighting routine
async def onlinetimeweighting(channel):
    nowtime = now.hour

    for r in range(len(dayweights)):
        if r == nowtime:   
            if dayweights[nowtime] < 10:
                dayweights[nowtime] += 1  
            else:
                pass
        else:
            if dayweights[r] != 0:
                dayweights[r] -= 1
            elif dayweights[r] == 0:
                pass

    completefilename = os.path.join(dir+'/'+channel, 'weighting.tmp')
    arrayfile = open(completefilename, 'w')
    print('📄⬆️ file written:', completefilename)
    arrayfile.write(str(dayweights))
    arrayfile.close()
    
async def analyseweights():
    maxval = max(dayweights)
    results = []

    if maxval != 0:
        for r in range(len(dayweights)):
            if dayweights[r] == maxval:
                results.append(r)
    else:
        return 'array error'
    
    return results
    
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
    print("⬇️ starting download")
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
    global dayweights
    try:
        completefilename = os.path.join(dir+'/'+channel, 'weighting.tmp')
        arrayfile = open(completefilename,"r")
        print('📄⬇️ file loaded:', completefilename)
        dayweights = ast.literal_eval(arrayfile.read())
        arrayfile.close()
        if dayweights == 0:
            print(errror)
    except:
        dayweights = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

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
            await onlinetimeweighting(channel)
            await sub0(channel)
        else:
            #print("⚫ channel: "+channel+" is offline")
            weights = await analyseweights()
            for hour in weights:
                if hour == now.hour:
                    #print("🕚 sleep for a minute")
                    await trio.sleep(60)
                else:
                    #print("🕚 sleep for 10 minute")
                    await trio.sleep(600)


async def main():
    print("🧑‍🤝‍🧑 starting threads")

    async with trio.open_nursery() as nursery:
        for line in Lines:
            if not line.rstrip():
                pass
            else:
            	nursery.start_soon(starup, line.rstrip())

trio.run(main)
