import os


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


def 进程_结束(process_name):
    # def process_kill(process_name):
    # cmd = 'taskkill /f /im wuauclt.exe'  # 代码原型:
    # os.system('taskkill /f /im wuauclt.exe')
    if not process_name.endswith(".exe"):
        process_name += ".exe"
    cmd = 'taskkill /f /im {}'.format(process_name)
    with os.popen(cmd) as f:
        print(f.read())


def tasklist_fi(process_name="闹钟_by雪天"):
    """根据指定的进程名称  输出 列表 """

    # cmd = 'tasklist /fi "imagename eq java.exe"'  # 信息: 没有运行的任务匹配指定标准。

    # cmd = 'tasklist /fi "imagename eq iexplore.exe"'  # 信息
    # cmd = 'tasklist /fi "imagename eq 闹钟_by雪天.exe"'  # 信息
    # cmd = 'tasklist /fi "imagename eq 闹钟_by雪天.exe" /FO LIST'  # 信息格式 输出为LIST
    '''默认table 格式
    映像名称                       PID 会话名              会话#       内存使用
    ========================= ======== ================ =========== ============
    iexplore.exe                 24364 Console                    1     33,864 K
    iexplore.exe                 11700 Console                    1    124,116 K
    '''
    if not process_name.endswith(".exe"):
        process_name += ".exe"

    cmd = 'tasklist /fi "imagename eq {}"'.format(process_name)

    with os.popen(cmd) as f:
        r = f.read()
        # print(f.read())
    print(r)
    # --> demo
    return r


def 进程_取pid(process_name="iexplore"):
    """
    参数:进程名称
    作用:取出全部pid
    返回值:list 文本型  ['20068', '22776']   如果没有这个进程 就是 []
    """
    # def process_pid(process_name="闹钟_by雪天"):
    # cmd = 'tasklist /fi "imagename eq java.exe"'  # 信息: 没有运行的任务匹配指定标准。

    # cmd = 'tasklist /fi "imagename eq iexplore.exe"'  # 信息
    # cmd = 'tasklist /fi "imagename eq 闹钟_by雪天.exe"'  # 信息
    # cmd = 'tasklist /fi "imagename eq 闹钟_by雪天.exe" /FO LIST'  # 信息格式 输出为LIST
    '''默认table 格式
    映像名称                       PID 会话名              会话#       内存使用
    ========================= ======== ================ =========== ============
    iexplore.exe                 24364 Console                    1     33,864 K
    iexplore.exe                 11700 Console                    1    124,116 K
    '''
    if not process_name.endswith(".exe"):
        process_name += ".exe"

    cmd = 'tasklist /fi "imagename eq {}"'.format(process_name)

    with os.popen(cmd) as f:
        r = f.read()
        # print(f.read())
    # print(r)
    # return r  --> demo  #■ 到这里为止 就是输出信息了  下面要取pid列表

    # r_list= r.split("\n")
    # print(r_list)
    # for i in r_list:
    # for i in range(len(r_list)):
    # if process_name in r_list[i]:
    #     print(r_list[i])
    # for n in r_list[i]:
    #     print(ord(n))  # 调试 发现 :中间的是 空格符
    # print(r_list[i].encode(b))  -->错误
    # print(bytes(r_list[i], encoding="utf-8"))  --> 错 不是想要的unicode字符

    # ■■这里
    # 1.正则可以取  process_name[\s]+([0-9]*)[\s]+
    # 2.文本 批量取中间 也可以  取完要去掉空格字符
    # ■□发现 其实csv格式的更好批量取文本 CSV是这种 "iexplore.exe","16004","Console","1","33,140 K" 前面文本exe"," 后面文本"
    lis = 文本_取中间_批量(r, process_name, "Console")
    for i in range(len(lis)):
        lis[i] = lis[i].strip()  #

    return lis
