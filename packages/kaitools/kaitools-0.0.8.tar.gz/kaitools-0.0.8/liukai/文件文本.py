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



def 文本_子文本替换(string, old, new, *count):
    # string=''
    return string.replace(old, new, *count)  # replace 不会改变原 string 的内容。 需要接收方 接收新的值


# 文本_读入文本   #一.文件不存在   二.文件编码是gbk /文件编码是utf8
def 文件_读入文本(file):
    try:
        with open(file, mode="r", encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # print('检测到编码可能是gbk,正在调用gbk...请稍候...')
        with open(file, mode="r", encoding='gbk') as f:
            return f.read()


def 文件_是否存在(path):
    import os
    return os.path.isfile(path)  # 这里需要是绝对路径 相对路径无法判断 -->3.6版本好像可以接受相对路径


def 文件_取运行目录():
    import os
    return os.getcwd()  # 当前xx.py文件的目录


def 文件夹_是否存在(path):
    import os
    return os.path.isdir(path)


def 文件夹_创建(path):
    import os
    if not os.path.isdir(path):  # 文件夹不存在
        os.makedirs(path)  # 文件夹 创建
    # 调试版:↓↓↓
    # if os.path.isdir(path):
    #     print(path,"已经存在")
    # else:
    #     print(path,"不存在,即将创建")
    #     os.makedirs(path)


def 文件_是否存在___废弃(file, 只判断文件=True):
    # ■废弃原因:因为  os.path.isfile 直接可以判断 同时 文件夹 是否存在做了另外个函数

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


def 文件路径_取_名称_后缀(path):
    # ■后缀格式如".py" ".txt" 包含"."符号
    import os
    # ■这里无法分离相对路径的 需要转换为绝对路径
    path = os.path.realpath(path)  # 转换为绝对路径
    path_dir, path_fname = os.path.split(path)  # 取文件夹名和文件名
    filename, extension = os.path.splitext(path_fname)  # 取文件名前面和后缀
    return filename, extension


def 文件路径_取_目录_文件名(path):
    import os
    # ■这里无法分离相对路径的 需要转换为绝对路径
    path = os.path.realpath(path)  # 转换为绝对路径
    path_dir, path_fname = os.path.split(path)
    return path_dir, path_fname


def 文件路径_取目录(path):
    import os
    return os.path.dirname(os.path.realpath(path))


def 文件路径_取文件名(path):
    import os
    return os.path.basename(os.path.realpath(path))


def 文件_更名(file_oldname, file_newname):
    # os.renames(old, new)
    import os
    # todo 需要判断文件是否存在吗??
    # os.rename(old_file_path, new_file_path), 只能对相应的文件进行重命名, 不能重命名文件的上级目录名.
    # os.renames(old_file_path, new_file_path), 是os.rename的升级版, 既可以重命名文件, 也可以重命名文件的上级目录名
    os.renames(file_oldname, file_newname)


def 文件_移动(old, new):
    import os
    import shutil
    # shutil.move(old, new)  # 移动文件  基本写法

    # 1. old文件要存在
    # 2. new文件所在文件夹要存在
    # TODO 3. 如果new文件已经 存在 如何处理? 覆盖? shutil.move 是会覆盖的
    if not os.path.isfile(old):
        print(old, "not exist!")
    else:
        new_dir, new_filename = os.path.split(new)  # 分离目标路径的 文件夹和文件名
        if not os.path.isdir(new_dir):  # 如果 目标文件夹 不存在
            print(new_dir, "not exist!")
            os.makedirs(new_dir)  # 创建 文件夹
        shutil.move(old, new)  # 移动 文件
        print("文件_移动  {} -> {}".format(old, new))


def 文本_写到文件(file, text):
    # 覆盖式写入
    import os
    file = os.path.realpath(file)  # 1. 转换为绝对路径  相对路径用下面的方法是取不到目录的
    file_dir = os.path.dirname(file)  # 2. 取目录 用于:检查文件多级目录是否存在  # 2.1 dir会与内置方法dir()重名 会导致内置方法无效  这里用file_dir
    if not os.path.isdir(file_dir): os.makedirs(file_dir)  # 3. 检查文件多级目录是否存在,如果不存在则创建目录

    with open(file, 'w', encoding='utf-8') as f:
        f.write(text)


# 文本_追加文本  #往文件 追加 不是覆写  可选参数:结尾是否添加换行符 默认为真
def 文本_追加文本(file, data, mode=True):
    """
    file:文件路径
    data:追加的数据
    mode:结尾是否增加换行,默认为假 -->改为默认为真
    """

    import os
    file = os.path.realpath(file)  # 1. 转换为绝对路径  相对路径用下面的方法是取不到目录的
    file_dir = os.path.dirname(file)  # 2. 取目录 用于:检查文件多级目录是否存在  # 2.1 dir会与内置方法dir()重名 会导致内置方法无效  这里用file_dir
    if not os.path.isdir(file_dir): os.makedirs(file_dir)  # 3. 检查文件多级目录是否存在,如果不存在则创建目录

    # 追加方式  "a+" 打开文件
    with open(file, mode="a+", encoding='utf-8') as f:
        # 如果模式==True 添加自动换行  模式==False 直接追加文本
        f.write(data + '\n') if mode else f.write(data)


def 文本_取中间文本(string, front, behind):
    # 返回值:None 或者 符合条件的string

    front_pos = string.find(front)

    if front_pos == -1:
        return None

    start_pos = front_pos + len(front)  # 修改 find文本 起始位置

    behind_pos = string.find(behind, start_pos)

    if behind_pos == -1:
        return None

    return string[start_pos:behind_pos]


def 文本_取中间_批量(string, front, behind):
    # 返回值 : [] 或 [string1,string2,...]
    # 示例:文本_取中间_批量('0123450123445','23','5') -->> ['4','44']
    # 示例:文本_取中间_批量('0123450123445','236','5') -->>[]

    lis = []

    start_pos = 0
    while True:
        front_pos = string.find(front, start_pos)

        if front_pos == -1:
            break

        start_pos = front_pos + len(front)  # 修改 find文本 起始位置

        behind_pos = string.find(behind, start_pos)

        if behind_pos == -1:
            break

        lis.append(string[start_pos:behind_pos])  # 加入列表

        start_pos = behind_pos + len(behind)  # 修改 find文本 起始位置 为 后面文本的下一个

    return lis


# 正则  #文本_取中间文本   文本_取中间文本
def 文本_取中间文本_正则_(string, front, behind):
    # ■□2020年10月20日更新: 涉及元字符转义 不推荐
    # def 文本_取中间文本(string, front, behind, 标识自动转义=False):
    # 返回值:None 或者 str1
    # 示例1:文本_取中间文本('0123450123445','23','5') -->> '4'
    # 示例1:文本_取中间_批量('0123450123445','236','5') -->>None
    import re
    # search 只查1次  #符合条件就停止
    # re.search(正则表达式,string,re.S)会返回一个对象,然后对该对象使用.group(i)方法  #备注:这里是因为正则有分组(.*?) 所以才是.group(1)
    # print(re.search(front + '(.*?)' + behind, string, re.S))
    # print(re.search(front + '(.*?)' + behind, string, re.S).group(0))
    # return re.search(front + '(.*?)' + behind, string, re.S).group(1)   #■★bug:当无匹配时,返回值None是没有group方法的

    # front和behind 里面如果有元字符 比如() 就需要处理 否则影响正则表达式 导致取出None
    '''
    if 标识自动转义:
        for i in ".*?()[]":
            if i in front:         front = re.sub('[{}]'.format(i), "\\" + i, front)
            if i in behind:        behind = re.sub('[{}]'.format(i), "\\" + i, behind)
            # front = re.sub('[%s]' % i, "\\" + i, front)
            # behind = re.sub('[%s]' % i, "\\" + i, behind)
            # 原先问题:不去判断 正则直接替换的话 会报错 : FutureWarning: Possible nested set at position 1
    '''
    for i in ".*?()[]+-":  # TODO 可能还有问题 因为元字符 还包括 xxxxxxxxxxx 等等
        # front = front.replace(i, "\\" + i)
        # behind = behind.replace(i, "\\" + i)
        if i in front:          front = front.replace(i, "\\" + i)
        if i in behind:         behind = behind.replace(i, "\\" + i)
        # 【知识点:】如果不判断是否存在 直接使用替换时, replace方式 都不会报错
    #  ■ 之所以要转义  是因为比如 (121977522)要取(和)之间的文本 使用front + '(.*?)' + behind就出错了

    r = re.search(front + '(.*?)' + behind, string, re.S)
    return r.group(1) if r else None  # 问题:这里是否要改成""? 因为很多时候 是str1+str2+..这种组合来的?
    # return r.group(1) if r else r   #因为当r为None时 return r 等同于None


# 文本_取中间_批量   #正则
def 文本_取中间_批量_正则_(string, front, behind):
    # ■□2020年10月20日更新: 涉及元字符转义 不推荐
    # def 文本_取中间_批量(string, front, behind, 标识自动转义=False):
    # 返回值:[] 或者 [str1,str2,...]
    # 示例1:文本_取中间_批量('0123450123445','23','5') -->> ['4','44']
    # 示例1:文本_取中间_批量('0123450123445','236','5') -->>[]
    """
    >>> 文本_取中间_批量('0123450123445','23','5')
    ['4', '44']
    >>> 文本_取中间_批量('0123450123445','236','5')
    []
    """
    import re

    # front和behind 里面如果有元字符 比如() 就需要处理 否则影响正则表达式 导致取出None
    '''
    if 标识自动转义:
        for i in ".*?()[]":
            if i in front:         front = re.sub('[{}]'.format(i), "\\" + i, front)
            if i in behind:        behind = re.sub('[{}]'.format(i), "\\" + i, behind)
            # front = re.sub('[%s]' % i, "\\" + i, front)
            # behind = re.sub('[%s]' % i, "\\" + i, behind)
            # 原先问题:不去判断 正则直接替换的话 会报错 : FutureWarning: Possible nested set at position 1
    '''

    for i in ".*?()[]":  # TODO 可能还有问题 因为元字符 还包括 + - \ ^ { } 等等
        # front = front.replace(i, "\\" + i)
        # behind = behind.replace(i, "\\" + i)
        if i in front:          front = front.replace(i, "\\" + i)
        if i in behind:         behind = behind.replace(i, "\\" + i)
        # 【知识点:】如果不判断是否存在 直接使用替换时, replace方式 都不会报错

    # re.S 表示“.”（不包含外侧双引号，下同）的作用扩展到整个字符串，包括“\n”
    return re.findall(front + '(.*?)' + behind, string, re.S)


# 检验是否含有中文字符
def 文本_是否包含汉字(string):
    """
    >>> 文本_是否包含汉字('123ni你好asasa')
    True
    >>> 文本_是否包含汉字('123niasasa')
    False
    >>> 文本_是否包含汉字('123')
    False
    >>> 文本_是否包含汉字('a')
    False
    >>> 文本_是否包含汉字('你')
    True
    >>> 文本_是否包含汉字('1')
    False
    """
    for i in string:
        if '\u4e00' <= i <= '\u9fa5':
            # if '一' <= i <= '龥':
            return True
    # 循环完毕 都还没返回 那结果就是False了
    return False


def 文本_取汉字(string):
    # 返回:列表  空列表[]  或者 有数据的列表
    # Failed example:    文本_取汉字('能取group取值')
    # Expected:    ['能取','取值']
    # Got: ['能取', '取值']
    #     >>> if None:print('代码示例:')
    """
    >>> 文本_取汉字('你好gro哈哈up呵呵')
    ['你好', '哈哈', '呵呵']
    >>> 文本_取汉字('123aaaa121212')   #测试
    []
    # >>> if False:print("其他测试用例:--------------------------+----------------------------")
    >>> 文本_取汉字('你123a你好吗aaa文本')
    ['你', '你好吗', '文本']
    >>> 文本_取汉字('1')
    []
    >>> 文本_取汉字('a')
    []
    """
    import re
    # return re.compile("[\u4e00-\u9fa5]").findall(文本)
    return re.compile("[\u4e00-\u9fa5]+").findall(string)  # 备注:这种是返回列表  并且没有re.S注释掉换行符
    # search的问题:需要对re.search返回的对象进行判断,不是None才能取group取值.
    # return re.compile("[\u4e00-\u9fa5]+",re.S).search(string).group()   #这种是返回单条数据 并且注释掉换行符 要对其对象是否None判断后 再对其group取值
    # return re.compile("[\u4e00-\u9fa5]+",re.S).search(string).group()   #这种是返回单条数据 并且注释掉换行符 要对其对象是否None判断后 再对其group取值
    # return re.search("[\u4e00-\u9fa5]+",string,re.S).group()   #这种是返回单条数据对象 并且注释掉换行符 要对其对象是否None判断后 再对其group取值


def 文本_取英文数字(string):
    # 返回: 列表  空列表[]  或者 有数据的列表
    import re
    return re.compile("[a-zA-Z0-9]+").findall(string)  # 连在一起的会一起加入列表  #没有+号 会返回1个个的匹配对象


def 文本_取数字(string):
    # 返回列表  空列表[]  或者 有数据的列表
    """
    >>> 文本_取数字('00abbbb12你3334好013549abcde')
    ['00', '12', '3334', '013549']
    >>> 文本_取数字('accva')
    []
    """
    import re
    # return re.compile("[0-9]").findall(文本)  #这种会返回1个个的数字
    return re.compile("[0-9]+").findall(string)  # 连在一起的数字会一起加入列表  #可行
    # return re.compile("\d+").findall(string)  #连在一起的数字会一起加入列表 #这个也行  \d和\\d都可以


def 文件_图片写到文件(file, data):
    import os
    file = os.path.realpath(file)  # 1. 转换为绝对路径  相对路径用下面的方法是取不到目录的
    file_dir = os.path.dirname(file)  # 2. 取目录 用于:检查文件多级目录是否存在  # 2.1 dir会与内置方法dir()重名 会导致内置方法无效  这里用file_dir
    if not os.path.isdir(file_dir): os.makedirs(file_dir)  # 3. 检查文件多级目录是否存在,如果不存在则创建目录

    # 多用于 图片字节集 写到本地图片
    with open(file, "wb") as f:
        f.write(data)



if __name__ == '__main__':
    _dict = 文件_取出字典('dict.txt')
    print(_dict)
    字典_写到文件(_dict, 'dict.txt')

