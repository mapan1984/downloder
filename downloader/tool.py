import os
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

def mkdir(path):
    """ 根据path创建目录 """
    path = path.strip()
    path = path.rstrip('\\')

    is_exist = os.path.exists(path)
    if is_exist:
        print("%s already exist." % path)
    else:
        os.makedirs(path)
        print("creat %s success." % path)


def open_url(request, timeout=60):
    try:
        response = urlopen(request, timeout=timeout)
    except HTTPError as error:
        print("The server couldn't fulfill the request.")
        print("URL: {}".format(request.full_url))
        print("Error code: ", error.code)
        raise
    except URLError as error:
        print("We failed to reach a server.")
        print("URLError: {}".format(request.full_url))
        print("Reason: ", error.reason)
        raise
    else:
        return response

def make_process_bar(total, init_has_load=0):
    """ 构建process_bar, 显示进度条
    argv:
        total：文件总字节数
        init_has_load：已下载字节数
    use:
        process_bar = make_process_bar(total, init_has_load=0)
        process_bar(has_load)
    """
    done_num = int(init_has_load/total * 100)
    print("[{done_str}{empty_str}]{done_num}%".format(
            done_str=">"*done_num, empty_str=" "*(100-done_num),
            done_num=done_num),
          end='\r')

    def process_bar(has_load):
        """ 传入has_load，显示进度 """
        nonlocal done_num
        new_done_num = int(has_load/total * 100)
        if done_num != new_done_num:
            done_num = new_done_num
            rest_num = 100 - done_num
            print("[{done_str}{empty_str}]{done_num}%".format(
                    done_str=">"*done_num, empty_str=" "*(rest_num),
                    done_num=done_num),
                  end='\r')
        if done_num == 100:
            print()

    return process_bar
