Mit open courseware lecture videos downloader.

Mit open courseware课程视频下载器。

#How to
You can find the mit open courseware course list [here](http://ocw.mit.edu/courses/). For those courses with lecture videos, you can download them all. Check out the download link, you will find a URL contains all the resources on Internet Archive.

1. Use the url to initialize a `Downloader` instance

    mit = Downloader("http://ia801502.us.archive.org/6/items/MIT6.006F11/")

2. Use the `download` method to download

    mit.download()

#如何使用

你可以在[这里](http://ocw.mit.edu/courses/)找到所有相关课程的列表，对于那些有上课视频的课程，所有的视频都是可以下载的。找到下载链接，里面是一个包含所有资源的Internet Archive的列表。

1. 使用上面找到的资源地址初始化一个下载器的实例

    mit = Downloader("http://ia801502.us.archive.org/6/items/MIT6.006F11/")

2. 使用实例的`download`方法进行下载

    mit.donwload()
