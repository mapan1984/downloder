import os.path
import argparse

from config import DOWNLOAD_DIR
from downloader import Downloader

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=str,
                        help="get the sourse file url")
    parser.add_argument("-f", "--file", type=str,
                        help="point the download file name")
    parser.add_argument("-t", "--thread", type=int, default=4,
                        help="point downloader thread number")
    args = parser.parse_args()
    url = args.url
    if args.file:
        filename = args.file
    else:
        filename = os.path.basename(url) or "download"
    dest = os.path.join(DOWNLOAD_DIR, filename)
    thread_num = args.thread
    downloader = Downloader(url, dest, thread_num=thread_num)
    downloader.run()
