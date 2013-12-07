# -*- coding: utf-8 -*-
import cgi
from string import Template
from playLrc import lrc2JsArray

form = cgi.FieldStorage()

name = form.getvalue('name', '')

def getOutput(templateFile, dict = {}):
    with open(templateFile) as f:
        if dict == {}:
            out = f.read()
        else:
            out = Template(f.read()).substitute(dict)
    return out
path = 'files/'

arr, mfile = '', ''
if name != '':
    arr = lrc2JsArray(path + name + '.lrc')
    mfile = '"' + path + name + '.mp3"'

print "Content-type: text/html"
print
#print "<html><head></head><body>"
#for i in range(5):
#    print str(i) + " Hello World!<br>"
#
#print "<br><br> Your name is %s" % (name,)

#print "</body></html>"

print getOutput("lrc.html", {'lyricarray':arr,'musicfile':mfile})
