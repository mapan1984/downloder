import queue
import threading
from urllib.request import Request

from downloader.tool import open_url

class Producer(threading.Thread):
    def __init__(self, url, _start, end, queue):
        super(Producer, self).__init__()
        self.url = url
        self._start = _start
        self.end = end
        print("<%s producer before> - start: %s; end: %s"
              % (threading.current_thread().name, self._start, self.end))
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
            'Range':'bytes={start}-{end}'.format(start=_start, end=end),
            'Accept-Encoding':'*',
        }
        self.queue = queue

    def run(self):
        request = Request(self.url, headers=self.headers)
        response = open_url(request)
        while True:
            content = response.read(1024)
            self.queue.put(content)
            self._start += len(content)
            if len(content) == 0:
                print("<%s producer after> - start: %s; end: %s"
                      % (threading.current_thread().name,
                         self._start, self.end))
                break
        response.close()

class Consumer(threading.Thread):
    def __init__(self, filename, _start, end, queue):
        super(Consumer, self).__init__()
        self.filename = filename
        self._start = _start
        self.end = end
        print("<%s consumer before> - start: %s; end: %s"
              % (threading.current_thread().name, self._start, self.end))
        self.queue = queue

    def run(self):
        file = open(self.filename, "wb")
        file.seek(self._start)
        while True:
            content = self.queue.get()
            self._start += len(content)
            file.write(content)
            self.queue.task_done()
            if self._start >= self.end:
                print("<%s consumer after> - start: %s; end: %s"
                      % (threading.current_thread().name,
                         self._start, self.end))
                break
        file.close()

class RangeDownloader(threading.Thread):
    def __init__(self, url, filename, _start, end):
        super(RangeDownloader, self).__init__()
        self.queue = queue.Queue()
        self.producer = Producer(url, _start, end, self.queue)
        self.consumer = Consumer(filename, _start, end, self.queue)

    def run(self):
        self.producer.start()
        self.consumer.start()
        self.producer.join()
        self.consumer.join()
