# -*- coding: utf-8 -*-

"""
mit的课程都放在Internet Archive上，每个课程有一个资源列表，需要的是课程的MP4课程。
目录下面会有一个xml文件，里面有全部的信息，下面的程序主要用于处理xml文件。
"""

from bs4 import BeautifulSoup
import urllib2
import urllib
import re
import xml.etree.ElementTree as ET
import time
import sys
#import subprocess

url = "http://ia801502.us.archive.org/6/items/MIT6.006F11/"

#url = 'http://ia600401.us.archive.org/8/items/MIT_Structure_of_Computer_Programs_1986/'

req = urllib2.Request(url, headers={'User-Agent': "Magic Browser"})
resp = urllib2.urlopen(req)
respHTML = resp.read()

soup = BeautifulSoup(respHTML)

#for tag in soup.find_all('a',text=re.compile("lec.*mp4")):
    #print tag

for tag in soup.find_all("a", text=re.compile("(?<!meta)\.xml")):
    xmlurl = tag.get("href")

#print xmlurl

req = urllib2.Request(url + xmlurl, headers={'User-Agent': "Magic Browser"})
resp = urllib2.urlopen(req)
respxml = resp.read()

#print type(respxml)

root = ET.fromstring(respxml)

dllist = []
for item in root:
    if re.search("lec.*mp4", item.get('name')):
        #print item.get('name')
#    if re.match("mp4", item.get('name')):
        print item.get('name')
        dllist.append(item.get("name"))

#print dllist
        #print item.get("name")
    #print item.tag, item.get('name')
    #print type(item.get('name'))
    #print type(child)
    #for child in item.iter():
        #print child.tag, child.attrib, child.text


def dlProgress(count, block_size, total_size):
    progress_size = int(count * block_size / (1024 * 1024))
    percent = int(count * block_size * 100 / total_size)

    sys.stdout.write("\r...Complete: %d%%, %d MB" % (percent, progress_size))
    sys.stdout.flush()

while dllist:
    for item in dllist:
        try:
            print "Try downloading %s." % (item),
            urllib.urlretrieve(url + item, item, reporthook=dlProgress)
            print "Done. Remove %s from dllist." % (item)
            dllist.remove(item)
        except:
            print "Fail to down %s, will try again later." % (item)

    print "Will sleep for half an hour, will try to download then."
    time.sleep(1800)
    #print "Pop test[0]: ", test[0]
    #test.pop(0)
