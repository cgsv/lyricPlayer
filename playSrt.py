import os, re, sys, time, multiprocessing, subprocess, codecs

def getTimerange(line):
    line = line.strip()
    begin , end = line[:12], line[-12:]
    def getSeconds(data):
        return int(data[:2]) * 3600 + int(data[3:5]) * 60 + \
                int(data[6:8]) + float(data[9:])/1000
    return getSeconds(begin), getSeconds(end)

def isBlankline(line): return line.strip() == ''

def isTimeline(line): return '-->' in line

def playSrt(srtFile):
    f = codecs.open(srtFile, encoding='utf-8')
    tstart, tend = 0.0, 0.0
    state = 'INVALID'
    while True:
        line = f.readline()
        if line == '': return
        line = line.strip()
        if state == 'INVALID':
            if isTimeline(line): state = 'TIME'
        elif state == 'TIME':
            state = 'SUBTITLE'
        elif state == 'SUBTITLE':
            if isBlankline(line):
                state = 'INVALID'
                time.sleep(tend - tstart)
                os.system('cls')

        if state == 'TIME':
            time.sleep(getTimerange(line)[0] - tend)
            tstart, tend = getTimerange(line)
        elif state == 'SUBTITLE':
            print line
    f.close()

def playVideo(videoFile):
    subprocess.call('ffplay -loglevel quiet -x 600 -y 400 ' + videoFile, shell = True)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    multiprocessing.Process(target=playVideo, args=(r"F:\downton_abbey.4x03.720p_hdtv_x264-fov.mkv",)).start()
    multiprocessing.Process(target=playSrt, args=(r'F:\downton_abbey.4x03.720p_hdtv_x264-fov.chn.srt8',)).start()
