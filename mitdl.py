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


class Downloader(object):
    def __init__(self, url):
        self.url = url
        self.dllist = []
        self.xmlurl = ''

    def parseHtml(self):
        req = urllib2.Request(self.url, headers={'User-Agent':
                                                 "Magic Browser"})
        resp = urllib2.urlopen(req)
        respHTML = resp.read()

        soup = BeautifulSoup(respHTML)

        for tag in soup.find_all("a", text=re.compile("(?<!meta)\.xml")):
            self.xmlurl = tag.get("href")

    def parseXml(self):
        req = urllib2.Request(self.url + self.xmlurl,
                              headers={'User-Agent': "Magic Browser"})
        resp = urllib2.urlopen(req)
        respxml = resp.read()

        root = ET.fromstring(respxml)

        for item in root:
            if re.search("lec.*mp4", item.get('name')):
                self.dllist.append(item.get("name"))


def dlProgress(count, block_size, total_size):
    progress_size = int(count * block_size / (1024 * 1024))
    percent = int(count * block_size * 100 / total_size)

    sys.stdout.write("\r...Complete: %d%%, %d MB" % (percent, progress_size))
    sys.stdout.flush()

if __name__ == "__main__":
    mit = Downloader("http://ia801502.us.archive.org/6/items/MIT6.006F11/")
    mit.parseHtml()
    mit.parseXml()

    while mit.dllist:
        for item in mit.dllist:
            try:
                print "Try to download %s." % (item)
                urllib.urlretrieve(mit.url + item, item, reporthook=dlProgress)
                print "Done. Remove %s from dllist." % (item)
                mit.dllist.remove(item)
            except:
                print "Fail to down %s, will try again later." % (item)

        print "Will sleep for half an hour, will try to download then."
        time.sleep(1800)

#"http://ia801502.us.archive.org/6/items/MIT6.006F11/"
