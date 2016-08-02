# -*- coding: utf-8  -*-

'''
time diagrams generator using websequencediagrams.com
=====================================================

bitelxux@gmail.com 2013

Requisites
----------

* imagemagick
'''

import urllib
import re
import os
import sys

#style='plainuml'
#style='rose'
#style='qsd'
#style='napkin'
#style='vs2010'
#style='mscgen'
#style='omegapple'
style='modern-blue'
#style='earth'
#style='roundgreen'

def getSequenceDiagram( text, outputFile, style = 'default' ):
    request = {}
    request["message"] = text
    request["style"] = style
    request["apiVersion"] = "1"

    url = urllib.urlencode(request)

    f = urllib.urlopen("http://www.websequencediagrams.com/", url)
    line = f.readline()
    f.close()

    expr = re.compile("(\?(img|pdf|png|svg)=[a-zA-Z0-9]+)")
    m = expr.search(line)

    if m == None:
        print "Invalid response from server."
        return False

    urllib.urlretrieve("http://www.websequencediagrams.com/" + m.group(0),
            outputFile )

    return True

if __name__ == '__main__':
    fileName = sys.argv[1]
    baseName = os.path.splitext(fileName)[0]
    text = open(fileName).read()
    getSequenceDiagram( text, '%s.png' % baseName, style ) 
    
    # cortamos 14 pixels de la base y se extiende el marco un 10%
    cmd = "convert %s.png -crop '100%%x100%%+0-14' -gravity center -extent '110%%x110%%' %s.png" % (baseName, baseName)
    os.system(cmd)
    
    

    
    
