def 文本_取部分文本_前面(string, endstring):
    # 比如 0123456789  里面 要取出56前面的部分:01234
    # 返回值:None 或者 符合条件的string

    pos = string.find(endstring)  # 取:后面文本的起始位置

    if pos == -1:  # 如果没找到 返回 None
        return None

    return string[:pos]  # 返回 切片


def 文本_取部分文本_后面(string, startstring):
    # 比如 0123456789  里面 要取出56后面的部分:789
    # 返回值:None 或者 符合条件的string

    pos = string.find(startstring)  # 取:标识文本的起始位置

    if pos == -1:
        return None

    pos = pos + len(startstring)  # 截取的位置 应该以标识文本出现的位置+它自己的长度
    # 比如0123456789 56出现的位置是5 截取的位置应该是 5+文本长度2 正好是7

    return string[pos:]



def 文件_到list(file, 分隔符="\n"):
    import os

    li = []  # 判断文件的路径是否存在

    # 如果文件不存在 直接返回 空的列表
    if not os.path.isfile(file):
        return li

    # 下面就是文件存在的处理
    txt = 文件_读入文本(file)
    li = txt.split(分隔符)  # li = txt.split("\n")
    return li


def list_写到文件(li: list, file, 分隔符="\n"):
    # 这里没处理file是相对路径时 文件夹是否存在的问题吗? --> 在文本_写到文件里面
    text = 分隔符.join(li)
    文本_写到文件(file, text)


def 文件_取出字典(filepath):  # 文件_取出字典
    # def load_dict_from_file(filepath):  # 文件_取出字典
    dict_ = {}
    try:
        with open(filepath, 'r') as f:
            for line in f:
                key, value = line.strip().split(':')
                dict_[key] = value
    # except IOError as ioerr:
    except IOError:
        print("文件 %s 不存在" % filepath)

    return dict_


def 字典_写到文件(_dict, filepath):  # 字典_写到文件
    # def 字典_到文件(_dict, filepath):  # 字典_写到文件
    try:
        with open(filepath, 'w') as f:
            for key, value in _dict.items():
                f.write('%s:%s\n' % (key, value))
    # except IOError as IOError:
    except IOError:
        print("文件 %s 无法创建" % filepath)


def 文件_是否存在(file, 只判断文件=True):
    # import pathlib
    # return pathlib.Path(file).is_file()
    # 方法1:
    # import pathlib
    # print(pathlib.Path(file).exists())  # 无论是文件还是文件夹 存在 就存在
    # print(pathlib.Path(file).is_file())  # 如果没有这个文件,哪怕是同名文件夹 也不行
    # 方法2:
    # import os
    # print(os.path.exists(file))  # 无论是文件还是文件夹 存在 就存在
    # print(os.path.isfile(file))  # 如果没有这个文件,哪怕是同名文件夹 也不行
    import os
    if 只判断文件:
        return os.path.isfile(file)  # 只判断文件
    else:
        return os.path.exists(file)  # 该路径只要存在,无论是文件还是文件夹,都可以


# 文本_读入文本   #一.文件不存在   二.文件编码是gb2312? /文件编码是utf8?
def 文件_读入文本(file):
    try:
        with open(file, mode="r", encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # print('检测到编码可能是gbk,正在调用gbk...请稍候...')
        with open(file, mode="r", encoding='gbk') as f:
            return f.read()


# 覆写 覆盖写入
def 文本_写到文件(file, text):
    # 检查文件多级目录是否存在,如果不存在则创建目录
    import os
    directory = os.path.dirname(file)  # dir与内置方法dir()重名 会导致内置方法无效
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 覆盖式写入
    with open(file, 'w', encoding='utf-8') as f:
        f.write(text)


def 文本_到字典(text: str):  # 用来取postdata
    li = text.split("&")
    dic = {}
    for i in li:
        # temp_li=i.split("=")
        k, v = i.split("=")
        dic[k] = v
    return dic


def 字典_到文本(dic:dict):
    li=[]
    for k,v in dic.items():
        li.append(k+"="+v)
    return "&".join(li)


if __name__ == '__main__':
    _dict = 文件_取出字典('dict.txt')
    print(_dict)
    字典_写到文件(_dict, 'dict.txt')

