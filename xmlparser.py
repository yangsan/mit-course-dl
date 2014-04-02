# -*- coding: utf-8 -*-

"""
mit的课程都放在Internet Archive上，每个课程有一个资源列表，需要的是课程的MP4课程。
目录下面会有一个xml文件，里面有全部的信息，下面的程序主要用于处理xml文件。
"""

from bs4 import BeautifulSoup
import urllib2
import re
#import subprocess

#url = "http://ia801502.us.archive.org/6/items/MIT6.006F11/"

url = 'http://ia600401.us.archive.org/8/items/MIT_Structure_of_Computer_Programs_1986/'

req = urllib2.Request(url, headers={'User-Agent': "Magic Browser"})
resp = urllib2.urlopen(req)
respHTML = resp.read()

soup = BeautifulSoup(respHTML)

for tag in soup.find_all('a',text=re.compile("lec.*mp4")):
    print tag
