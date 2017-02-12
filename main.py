import sys
import os.path

from config import DOWNLOAD_DIR
from downloader import Downloader

if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) == 4:
        argv = sys.argv
        url = argv[1]
        filename = argv[2]
        thread_num = argv[3]
        downloader = Downloader(url, os.path.join(DOWNLOAD_DIR, filename),
                                thread_num=thread_num)
        downloader.run()
    else:
        url = input("url: ")
        filename = input("filename: ")
        thread_num = input("thread_num: ")
        downloader = Downloader(url, os.path.join(DOWNLOAD_DIR, filename),
                                thread_num=thread_num)
        downloader.run()
