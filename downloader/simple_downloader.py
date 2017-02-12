from urllib.request import Request

from downloader.tool import make_show_box, open_url

def download(url, filename, headers=None):
    """ download filename from url
    argv:
        url: str
        filename: str
    """
    request = Request(url, headers=headers)
    response = open_url(request)
    # 获取文件长度（单位Byte）
    file_length = int(response.info()['Content-length'])
    # 构造show_process_bar用于显示进度
    show_process_bar = make_show_box(file_length)
    # 打开文件用于写入
    file = open(filename, "wb")

    # 不断将获取内容写入文件
    content = response.read(1024)
    has_load = 0
    while content:
        once_write = file.write(content)
        has_load = has_load + once_write
        show_process_bar(has_load)
        content = response.read(1024)
    response.close()
    file.close()
