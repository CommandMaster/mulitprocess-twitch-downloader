import os
import modules.notification as notification
import subprocess
from datetime import datetime
import trio
from logbook import Logger, StreamHandler
import modules.twitter_bot as twitter_bot

async def dlstream(channel, filename, workdir):
    log = Logger(channel)
    #os.chdir(folder)
    
    url = 'https://www.twitch.tv/' + channel
    now = datetime.now()
    filename = now.strftime("%H.%M")
    tempfilename = "temp_1_" + filename  + ".mp4"
    tempfilename2 = "temp_2_" + filename + ".mp4"

    await notification.notification("starting download of: "+channel)
    log.info("🔽 download started")

    try:
        await trio.run_process(["streamlink", "twitch.tv/" + channel, 'best', "-o", workdir+tempfilename], stdout=subprocess.DEVNULL)
    except:
        pass


    log.info("🔴 Recording stream is done")
    await notification.notification("download done, start fixing")

    
    log.info("🧰 Fixing video file") 

    if(os.path.exists(workdir+tempfilename) is True):  
        try:
            await trio.run_process(['ffmpeg', '-loglevel', 'quiet', '-err_detect', 'ignore_err', '-i', workdir+tempfilename, '-c', 'copy', workdir+tempfilename2], stdout=subprocess.DEVNULL)
            log.info("🧰 file fixed")

            await trio.run_process(['ffmpeg', '-loglevel', 'quiet', '-i', workdir+tempfilename2, '-c:v', 'libx264', '-crf', '18', '-preset', 'slow', '-c:a', 'copy', workdir+filename + ".mp4"], stdout=subprocess.DEVNULL)
            log.info("🧰 file compressed")

        except Exception as e:  
            log.info(e)
        log.info("🗑️ deleted temp files!")

    else:  
        log.info("▶️ ▶️ Skip fixing and Compressing. File not found.")

    try:
        os.remove(workdir+tempfilename)
        os.remove(workdir+tempfilename2)
    except:
        pass

    await notification.notification("process done of: " + channel)
        #trio.run_process(['arch', '-x86_64', '$(which python3)', '-m', '/Users/eliasmaurer/Documents/twitch-downloader/versions/v2/modules/twitter_bot.py', 'gott', workdir, folder])
    await trio.sleep(3)
    return filename