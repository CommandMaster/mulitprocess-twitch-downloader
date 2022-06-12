import datetime
import os
from ast import literal_eval
from logbook import Logger, StreamHandler

now = datetime.datetime.now()
dir = os.environ.get("DIR")

async def readstate(channel):
    global dayweights
    log = Logger(channel)
    try:
        completefilename = dir+'/'+channel+'/weighting.tmp'
        arrayfile = open(completefilename)
        dayweightss = arrayfile.read()
        dayweights = literal_eval(dayweightss)
        arrayfile.close()
        if dayweights == 0:
            log.info(errror)
    except:
        completefilename = dir+'/'+channel+'/weighting.tmp'
        log.info('error no weight data, creating blank')
        arrayfile = open(completefilename, "a")
        text = '📄⬆️ file written: '+ completefilename
        log.info(text)
        arrayfile.write('[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]')
        arrayfile.close()
        dayweights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    log.info('📄⬇️ loaded: '+str(dayweights)+', out of: '+completefilename)
#hour weighting routine
async def onlinetimeweighting(channel):
    nowtime = now.hour
    log = Logger(channel)
    
    for r in range(len(dayweights)):
        if r == nowtime:   
            if dayweights[nowtime] < 10:
                dayweights[nowtime] += 1  
            else:
                pass
        else:
            if dayweights[r] != 0:
                dayweights[r] -= 0.5
            elif dayweights[r] == 0:
                pass

    completefilename = os.path.join(dir+'/'+channel, 'weighting.tmp')
    arrayfile = open(completefilename, 'w')
    arrayfile.write(str(dayweights))
    arrayfile.close()
    log.info('📄⬆️ written: '+str(dayweights)+', to: '+completefilename)
    
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