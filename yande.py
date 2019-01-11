import os  # 引入文件模块
import re  # 正则表达式
import urllib.request
import multiprocessing


# 连接网页并返回源码
def open_url(url):
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent",
                       "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/55.0.2883.87 Safari/537.36")
        response = urllib.request.urlopen(req)
        status_code = response.code
        html = response.read()
        return html
    except Exception as e:
        print(e)
        return 404


def mkdir(path):
    """
    :param path: 路径
    :return:
    """
    # 引入模块
    import os

    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    is_exists = os.path.exists(path)

    # 判断结果
    if not is_exists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False


def yande1(pages1, pages2, number):
    mkdir('img')
    for i in range(pages1, pages2 + 1):
        imgs = 1
        print(i)
        url = 'https://yande.re/post?page=' + str(i)
        # print(url)
        local_folder = os.path.split(os.path.realpath(__file__))[0]
        folder = "{0}\\img\\page{1}".format(local_folder, i)
        print("线程{0}".format(number))
        mkdir(folder)
        os.chdir(folder)

        html = open_url(url)
        html = html.decode('gbk', 'ignore')
        img_adds = re.findall(r'<a class="directlink largeimg" href="([^"]+\.jpg)"', html)
        for j in img_adds:
            filename = str(imgs) + '.jpg'
            imgs += 1
            img_html = open_url(j)
            if img_html == 404:
                continue
            with open(filename, 'wb') as f:
                f.write(img_html)
                print("线程{0}".format(number))
                print(j + '下载完成....')


if __name__ == '__main__':
    number = int(input('请输入同步执行进程总数:'))
    proc_process_sequence = []
    for i in range(0, number):
        print("进程{0}".format(i))
        page1 = int(input('请输入你要下载的起始页面数：'))
        page2 = int(input('请输入你要下载的末尾页面数：'))
        proc_process_sequence.append(multiprocessing.Process(target=yande1, args=(page1, page2, i)))
    for i in proc_process_sequence:
        i.start()
    for i in proc_process_sequence:
        i.join()
