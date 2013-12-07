# -*- coding: utf-8 -*-
import re, sys, time, os, pyglet, multiprocessing, subprocess

def getTime(l):
    res = re.search('\[(\d\d):(\d\d\.\d\d)\]', l)
    if not res:
        return None
    return float(res.group(2)) + int(res.group(1)) * 60

def playLrc(lrcfile, singleLine = False):
    t = 0.0
    f = open(lrcfile)
    while True:
        data = f.readline()
        if data == '': break
        tnew = getTime(data)
        if tnew:
            time.sleep(tnew - t)
            if singleLine:
                os.system('cls')
            t = tnew
        pdata = re.sub('\[.*?\]','',data)
        if pdata != '\n':
            print ' ' * ((80 - len(pdata)) / 2) + pdata
    f.close()

def getTimeList(lrcfile):
    f = open(lrcfile)
    li = []
    while True:
        data = f.readline()
        if data == '': break
        tnew = getTime(data)
        if tnew:
            li.append([tnew,  re.sub('\[.*?\]','',data)])
    return li

def lrc2JsArray(lrcfile):
    ret = ''
    tcl =  getTimeList(lrcfile)
    tl = map(lambda x:x[0], tcl)
    cl = map(lambda x:x[1], tcl)
    tlint = [tl[0]]
    for i in range(len(tl) - 1):
        tlint.append(tl[i+1] - tl[i])
    tlint.append(1)
    cl.insert(0,'')
    ret += 'lt = '
    ret += str(map(lambda x:int(x*1000),tlint))
    ret += '; ll = ['
    for m in cl:
        ret += ('"'+m[:-1]+'",')
    ret += '];'
    return ret

def playMusic(musicFile):
    source = pyglet.media.load(musicFile)
    player = pyglet.media.Player()
    player.queue(source)
    player.play()

def playMusic2(musicFile):
    subprocess.call('ffplay -loglevel quiet ' + musicFile, shell = True)

if __name__ == '__main1__':
    os.system('cls')
    #playLrc('love.lrc')
    fname = sys.argv[1] if len(sys.argv) > 1 else 'love'
    multiprocessing.freeze_support()
    multiprocessing.Process(target=playMusic2, args=(fname + '.mp3',)).start()
    time.sleep(0.25)
    multiprocessing.Process(target=playLrc, args=(fname + '.lrc',)).start()


#print lrc2JsArray('love.lrc')
