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


def open_url(request):
    try:
        response = urlopen(request)
    except HTTPError as error:
        print("The server couldn't fulfill the request.")
        print("Error code: ", error.code)
        return None
    except URLError as error:
        print("We failed to reach a server.")
        print("Reason: ", error.reason)
        return None
    else:
        return response

def make_show_str(total, init_has_load=0):
    """构建返回process_bar_str的函数, 如果process_bar_str没有更新，返回None
    argv:
        total：文件总字节数
        init_has_load：已下载字节数
    use:
        get_process_bar = make_show_box(total, init_has_load=0)
        process_bar = get_process_bar(has_load)
    """
    done_num = int((init_has_load/total)*100)

    def get_process_bar(has_load):
        """ 传入has_load，构造进度str """
        nonlocal done_num    # 声明done_num
        new_done_num = int((has_load/total)*100)
        if done_num != new_done_num:
            done_num = new_done_num
            rest_num = 100 - done_num
            # 返回进度条字符串
            return "[" + ">"*done_num + " "*rest_num + "]"
        else:
            return None

    return get_process_bar

def make_show_box(total, init_has_load=0):
    """ 构建show_box, 显示进度条
    argv:
        total：文件总字节数
        init_has_load：已下载字节数
    use:
        show_process_bar = make_show_box(total, init_has_load=0)
        show_process_bar(has_load)
    """

    get_process_bar = make_show_str(total, init_has_load)

    def show_process_bar(has_load):
        """ 传入has_load，显示进度 """
        nonlocal get_process_bar
        process_bar_str = get_process_bar(has_load)
        if process_bar_str is None:
            pass
        else:
            # 刷新显示
            os.system("cls")
            print("download precess...")
            print("[has load/total: %d/%d]" % (has_load, total))
            print("%s" % process_bar_str, end='\r')

    return show_process_bar
