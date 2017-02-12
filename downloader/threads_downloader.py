import math
import threading
from urllib.request import Request

from downloader.tool import open_url
from downloader.range_downloader import RangeDownloader

class ThreadDownloader():

    def __init__(self, url, filename, thread_num=4):
        self.url = url
        self.filename = filename
        self.thread_num = int(thread_num)
        self._init_content_length()
        self.lock = threading.Lock()

    def _init_content_length(self):
        """ 使用HEAD请求response headers信息 """
        request = Request(self.url, method='HEAD')
        response = open_url(request)
        info = response.info()
        # support 'Range' request headers
        if info.get('Accept-Ranges') == 'bytes':
            self.content_length = int(info.get('Content-Length'))

    def _get_ranges(self):
        ranges = []
        offset = math.ceil(self.content_length//self.thread_num)
        print("offset: %s" % str(offset))
        # 每个线程取得区间
        for i in range(self.thread_num-1):
            ranges.append((i*offset, (i+1)*offset-1))
        ranges.append(((self.thread_num-1)*offset, self.content_length-1))
        return ranges

    def run(self):
        all_threads = []
        for num, ran in enumerate(self._get_ranges(), start=1):
            start, end = ran
            # print('thread %d start:%s,end:%s' % (num, start, end))
            # 开线程
            downloader = RangeDownloader(self.url, self.filename, start, end)
            downloader.start()
            all_threads.append(downloader)
        for thread in all_threads:
            thread.join()
        print('download %s load success' % self.filename)
