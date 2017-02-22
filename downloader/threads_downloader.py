import math
import threading
from urllib.request import Request

from downloader.tool import open_url
from downloader.range_downloader import RangeDownloader
from downloader.simple_downloader import download

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
        response.close()
        # support 'Range' request headers
        if info.get('Accept-Ranges') == 'bytes':
            self.content_length = int(info.get('Content-Length'))
        else:
            self.content_length = None

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
        if self.content_length:
            all_threads = []
            for ran in self._get_ranges():
                start, end = ran
                downloader = RangeDownloader(self.url, self.filename, start, end)
                downloader.start()
                all_threads.append(downloader)
            for thread in all_threads:
                thread.join()
        else:
            download(self.url, self.filename)
        print('download %s load success' % self.filename)
