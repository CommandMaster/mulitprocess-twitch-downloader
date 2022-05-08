import os
import notification
import log
import subprocess
from datetime import datetime
import trio

async def dlstream(channel, folder, workdir):
    #os.chdir(folder)
    
    url = 'https://www.twitch.tv/' + channel
    now = datetime.now()
    filename = now.strftime("%H.%M")
    tempfilename = "temp_1_" + filename  + ".mp4"
    tempfilename2 = "temp_2_" + filename + ".mp4"

    await notification.notification("starting download of: "+channel)
    log.printlog("🔽 download started, of: "+channel)

    try:
        await trio.run_process(["streamlink", "twitch.tv/" + channel, 'best', "-o", workdir+tempfilename], stdout=subprocess.DEVNULL)
    except:
        pass

    log.printlog("🔴 Recording stream is done, of: "+channel)
    log.printlog("🧰 Fixing video file, of: "+channel)
    await notification.notification("download done, stat fixing video of: " + channel)  

    if(os.path.exists(workdir+tempfilename) is True):  
        try:
            await trio.run_process(['ffmpeg', '-loglevel', 'quiet', '-err_detect', 'ignore_err', '-i', workdir+tempfilename, '-c', 'copy', workdir+tempfilename2], stdout=subprocess.DEVNULL)
            log.printlog("🧰 file fixed")

            await trio.run_process(['ffmpeg', '-loglevel', 'quiet', '-i', workdir+tempfilename2, '-c:v', 'libx264', '-crf', '18', '-preset', 'slow', '-c:a', 'copy', workdir+filename + ".mp4"], stdout=subprocess.DEVNULL)
            log.printlog("🧰 file compressed")

        except Exception as e:  
            log.printlog(e)
        log.printlog("🗑️ deleted temp files!")

    else:  
        log.printlog("▶️ ▶️ Skip fixing and Compressing. File not found.")

    try:
        os.remove(workdir+tempfilename)
        os.remove(workdir+tempfilename2)
    except:
        pass

    await notification.notification("process done of: " + channel)
    await trio.sleep(3)