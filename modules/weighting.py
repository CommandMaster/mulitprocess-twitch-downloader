import datetime
import modules.log as log
import os
from ast import literal_eval

now = datetime.datetime.now()
dir = os.environ.get("DIR")

async def readstate(channel):
    global dayweights
    completefilename = dir+'/'+channel+'/weighting.tmp'
    arrayfile = open(completefilename)
    text = '📄⬇️ file loaded: '+ completefilename
    log.printlog(text)
    dayweightss = arrayfile.read()
    dayweights = literal_eval(dayweightss)
    print(dayweights[21])
    arrayfile.close()
    if dayweights == 0:
        log.printlog(errror)
    
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
    text = '📄⬆️ file written: '+ completefilename
    log.printlog(text)
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