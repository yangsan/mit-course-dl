# -*- coding: utf-8 -*-

"""
MIT open courseware puts all its lecture videos on Internet Archive, and this
is a python script to download them.
mit的课程都放在Internet Archive上，每个课程有一个资源列表，需要的是课程的MP4课程。
这个脚本用于下载所有的视频。
"""

from bs4 import BeautifulSoup
import urllib2
import urllib
import re
import xml.etree.ElementTree as ET
import time
import sys
import os.path


class Downloader(object):
    """
    Downloader class need a URL where the videos are stored, and then you can
    use the Downloader.download method to download all the videos.
    使用视频资源的地址初始化一个Downloader的实例，使用该实例的download方法可以
    下载视频
    """
    def __init__(self, url):
        self.url = url
        self.dllist = []  # download list
        self.xmlurl = ''
        self.item = ''
        self.time = time.time()
        self.speed = 0

    def parseHtml(self):
        """
        This func parse the html the url returns, and find the .xml file.
        此函数解析上面url给出的网页，找到里面的xml文件
        """
        req = urllib2.Request(self.url, headers={'User-Agent':
                                                 "Magic Browser"})
        resp = urllib2.urlopen(req)
        respHTML = resp.read()

        soup = BeautifulSoup(respHTML)  # use beautiful soap to parse html

        for tag in soup.find_all("a", text=re.compile("(?<!meta)\.xml")):
            self.xmlurl = tag.get("href")

    def parseXml(self):
        """
        This func parse the .xml file, find all the name of lecture videos to
        build a download list.
        此函数解析上面给出的xml文件，找出里面所有视频课程的文件名，将其组成一个
        下载列表。
        """
        req = urllib2.Request(self.url + self.xmlurl,
                              headers={'User-Agent': "Magic Browser"})
        resp = urllib2.urlopen(req)
        respxml = resp.read()

        root = ET.fromstring(respxml)

        for item in root:
            name = item.get("name")
            if re.search("lec.*mp4", name):  # find all the lecture videos
                if not os.path.isfile(name):
                # check if the video was already there
                    self.dllist.append(name)

    def dowload(self):
        """
        Download all the videos according to download list.
        根据下载列表下载所有的视频文件。
        """

        self.parseHtml()
        self.parseXml()

        while self.dllist:
            for self.item in self.dllist:
                try:
                    print "Try to download %s." % (self.item)
                    urllib.urlretrieve(self.url + self.item, self.item,
                                       reporthook=self.dlProgress)
                    # use urllib.urlretrieve to download videos
                    print "\nDone. Remove %s from dllist." % (self.item)
                    # remove the one downloaded successfully
                    self.dllist.remove(self.item)
                except Exception as e:
                    print e
                    print "\nFail to down %s." % (self.item)

            if not self.dllist:
                print "Will sleep for half an hour, will try to download then."
                time.sleep(1800)
            else:
                print "Finishing downloading all."

    def dlProgress(self, count, block_size, total_size):
        """
        This func generate a download proccess indicater.
        这个函数会生成一个下载进度的展示。
        """
        progress_size = int(count * block_size / (1024 * 1024))
        percent = int(count * block_size * 100 / total_size)
        if count % 50 == 0:
            # compute the download speed every 50 block
            span = time.time() - self.time
            self.speed = int(50 * block_size / (1024 * span))
            self.time = time.time()

        sys.stdout.write("\rTry downloading %s : %d%%, %d MB, %d KB/s"
                         % (self.item, percent, progress_size, self.speed))
        # print the percent and speed to stdout which shows in terminal here
        # note the usage of \r at the begginning
        sys.stdout.flush()
        # print everything in cache to the screen, neccessary here

if __name__ == "__main__":
    """
    Use a url to initialize a Downloader instance, use the download method to
    download.
    用一个url初始化一个Downloader的实例，使用其中的download 方法下载视频。
    """
    mit = Downloader("http://ia801502.us.archive.org/6/items/MIT6.006F11/")
    mit.dowload()
