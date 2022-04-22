import os
import notification
import subprocess
from datetime import datetime
from rich import print
import trio

async def dlstream(channel, folder, dir):
    os.chdir(folder)
    
    url = 'https://www.twitch.tv/' + channel
    now = datetime.now()
    filename = now.strftime("%H.%M")
    tempfilename = "temp_1_" + filename  + ".mp4"
    tempfilename2 = "temp_2_" + filename + ".mp4"

    await notification.notification("starting download of: "+channel)
    print("🔽 download started, of: "+channel)

    await trio.run_process(["streamlink", "twitch.tv/" + channel, 'best', "-o", tempfilename], stdout=subprocess.DEVNULL)

    print("🔴 Recording stream is done, of: "+channel)
    print("🧰 Fixing video file, of: "+channel)
    await notification.notification("download done, stat fixing video of: " + channel)  

    if(os.path.exists(tempfilename) is True):  
        try:
            await trio.run_process(['ffmpeg', '-err_detect', 'ignore_err', '-i', tempfilename, '-c', 'copy', tempfilename2], stdout=subprocess.DEVNULL)
            print("🧰 file fixed")

            await trio.run_process(['ffmpeg', '-i', tempfilename2, '-c:v', 'libx264', '-crf', '18', '-preset', 'slow', '-c:a', 'copy', filename + ".mp4"], stdout=subprocess.DEVNULL)
            print("🧰 file compressed")

        except Exception as e:  
            print(e) 
        print("🗑️ deleted temp files!")

    else:  
        print("▶️ ▶️ Skip fixing and Compressing. File not found.")

    os.remove(tempfilename)
    os.remove(tempfilename2)

    await notification.notification("process done of: " + channel)

    os.chdir(dir)