import datetime

e = datetime.datetime.now()

def printlog(channel, text):
    print ("%s:%s:%s-%s/%s/%s" % (e.hour, e.minute, e.second, e.day, e.month, e.year), channel, text)
