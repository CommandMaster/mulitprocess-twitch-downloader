# mulitprocess-twitch-downloader📺⬇️

This Script is able to check a list of Streamers on Twitch.
Hereby multible streams can be downloaded at once, thanks to mulitprocess support by trio(https://trio.readthedocs.io)

## Installation

1.create virtual env

```bash
  pip install virtualenv
  virtualenv env
  source env/bin/acivate
```

2.requirumens

-python 3.x.x is used

```bash
  pip install requirumens.txt
  
  mac
  brew install ffmpeg

  linux
  sudo apt-get install ffmpeg -y
```

3.configure channellist and change requirumens in .env-example and change name of it into .env

##start

to start script

```bash
  source env/bin/activate
  python3 main.py
```
