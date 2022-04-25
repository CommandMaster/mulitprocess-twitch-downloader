import os
import notification
import subprocess
from datetime import datetime
from rich import print
import trio

async def dlstream(channel, folder, workdir):
    #os.chdir(folder)
    
    url = 'https://www.twitch.tv/' + channel
    now = datetime.now()
    filename = now.strftime("%H.%M")
    tempfilename = "temp_1_" + filename  + ".mp4"
    tempfilename2 = "temp_2_" + filename + ".mp4"

    await notification.notification("starting download of: "+channel)
    print("🔽 download started, of: "+channel)

    try:
        await trio.run_process(["streamlink", "twitch.tv/" + channel, 'best', "-o", workdir+tempfilename], stdout=subprocess.DEVNULL)
    except:
        pass
    
    print("🔴 Recording stream is done, of: "+channel)
    print("🧰 Fixing video file, of: "+channel)
    await notification.notification("download done, stat fixing video of: " + channel)  

    if(os.path.exists(workdir+tempfilename) is True):  
        try:
            await trio.run_process(['ffmpeg', '-err_detect', 'ignore_err', '-i', workdir+tempfilename, '-c', 'copy', workdir+tempfilename2], stdout=subprocess.DEVNULL)
            print("🧰 file fixed")

            await trio.run_process(['ffmpeg', '-i', workdir+tempfilename2, '-c:v', 'libx264', '-crf', '18', '-preset', 'slow', '-c:a', 'copy', workdir+filename + ".mp4"], stdout=subprocess.DEVNULL)
            print("🧰 file compressed")

        except Exception as e:  
            print(e)
        print("🗑️ deleted temp files!")

    else:  
        print("▶️ ▶️ Skip fixing and Compressing. File not found.")

    os.remove(workdir+tempfilename)
    os.remove(workdir+tempfilename2)

    await notification.notification("process done of: " + channel)
    await trio.sleep(3)