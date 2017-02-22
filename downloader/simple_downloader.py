from urllib.request import Request

from downloader.tool import make_process_bar, open_url

def download(url, filename, headers={}):
    """ download filename from url
    argv:
        url: str
        filename: str
    """
    request = Request(url, headers=headers)
    response = open_url(request)
    file_length = response.info().get('Content-Length')
    if file_length:
        file_length = int(file_length)
        process_bar = make_process_bar(file_length)
        file = open(filename, "wb")
        has_load = 0
        while True:
            content = response.read(1024)
            if not content:
                break
            once_write = file.write(content)
            has_load = has_load + once_write
            process_bar(has_load)
        response.close()
        file.close()
    else:
        file = open(filename, "wb")
        while True:
            content = response.read(1024)
            if not content:
                break
            once_write = file.write(content)
        response.close()
        file.close()

