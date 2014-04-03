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
import os.path
#import subprocess


class Downloader(object):
    def __init__(self, url):
        self.url = url
        self.dllist = []
        self.xmlurl = ''
        self.item = ''
        self.time = time.time()
        self.speed = 0

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
            name = item.get("name")
            if re.search("lec.*mp4", name):
                if not os.path.isfile(name):
                    self.dllist.append(name)

    def dowload(self):

        self.parseHtml()
        self.parseXml()

        while self.dllist:
            for self.item in self.dllist:
                try:
                    print "Try to download %s." % (self.item)
                    urllib.urlretrieve(self.url + self.item, self.item,
                                       reporthook=self.dlProgress)
                    print "\nDone. Remove %s from dllist." % (self.item)
                    self.dllist.remove(self.item)
                except Exception as e:
                    print e
                    print "\nFail to down %s." % (self.item)

            if not self.dllist:
                print "Will sleep for half an hour, will try to download then."
                time.sleep(1800)

    def dlProgress(self, count, block_size, total_size):
        progress_size = int(count * block_size / (1024 * 1024))
        percent = int(count * block_size * 100 / total_size)
        #print count
        if count % 50 == 0:
            self.speed = int(50 * block_size / (1024 * (time.time() - self.time)))
            self.time = time.time()

        sys.stdout.write("\rTry downloading %s : %d%%, %d MB, %d KB/s"
                         % (self.item, percent, progress_size, self.speed))
        sys.stdout.flush()

if __name__ == "__main__":
    mit = Downloader("http://ia801502.us.archive.org/6/items/MIT6.006F11/")
    mit.dowload()
