# print('成功导入我的demo', 'liukai.py')

def test():
    print("hi","kai","tools")

#
# def 系统_取桌面分辨率():
#     import ctypes
#     winapi = ctypes.windll.user32
#     x = winapi.GetSystemMetrics(0)
#     y = winapi.GetSystemMetrics(1)
#     print(x)
#     print(y)
#     # 1440
#     # 900
#     return x, y
#
#
# def 信息框(msg="信息提示", title="窗口标题"):
#     # 示例: 弹窗("my warning~!提示!")
#     import ctypes
#     ctypes.windll.user32.MessageBoxA(0, msg.encode('gb2312'), title.encode('gb2312'), 0)
#     # ctypes.windll.user32.MessageBoxA(0,msg.encode('utf-8'),title.encode('utf-8'),0) #★utf-8也会乱码
#     # ctypes.windll.user32.MessageBoxA(0,msg,title,0) #★原始位置只接受bytes 不编码就有问题
#     # ctypes.windll.user32.MessageBoxA(0,u"点击确定 开始处理data目录下面的xls文件,分析处理完成后会有提示.^_ ^".encode('gb2312'),u' 信息'.encode('gb2312'),0)
#
#
# def 注册表_强制刷新():
#     # 可以强制注册表生效 比如改完注册表后的环境变量
#     import ctypes
#
#     # 方式1 有时候会卡住 遇到过刷新注册表卡住 不结束
#     # ctypes.windll.user32.SendMessageW(65535, 26, 0, "Environment")  # -->可以刷新注册表
#     # ctypes.windll. 到这里就没智能提醒了
#
#     # 方式2:
#     HWND_BROADCAST = 0xFFFF
#     WM_SETTINGCHANGE = 0x1A
#     SMTO_ABORTIFHUNG = 0x0002
#     result = ctypes.c_long()
#     SendMessageTimeoutW = ctypes.windll.user32.SendMessageTimeoutW
#     SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, u'Environment', SMTO_ABORTIFHUNG, 5000, ctypes.byref(result))
#
#     # 写法2:
#     # c = ctypes.WinDLL("user32.dll")
#     # c.SendMessageW(65535, 26, 0, "Environment")
#
#     # 历史笔记:
#     # ctypes.windll.user32.SendMessage(65535, 26, 0, "Environment")  #-->无效 没有这个方法 AttributeError: function 'SendMessage' not found
#     # 百度 SendMessage  发现 是分为 SendMessageA SendMessageW
#     # 然后google搜索 "ctypes.windll.user32.SendMessage" 看到类似 SendMessage = ctypes.windll.user32.SendMessageW
#     # ctypes.windll.user32.SendMessageA(65535, 26, 0, "Environment")  #-->无效  不会报错 但是也无法刷新注册表
#     # ■ctypes.windll.user32.SendMessageW(65535, 26, 0, "Environment")  # -->可以刷新注册表
#
#     # 历史:方法: 需要win32gui win32api win32con 那些东西 很麻烦
#     # win32api.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SETTINGCHANGE, 0, "Environment")
#
#
# def timefunc(func):
#     # 作为装饰器使用，返回函数执行需要花费的时间
#     # 任意函数  只要def funcname(...)的上方加了@timefunc 就可以被装饰
#
#     import time
#     from functools import wraps
#
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         t = time.time()
#         result = func(*args, **kwargs)
#         print(func.__name__, "函数,总计耗时:", time.time() - t, "秒")
#         return result
#
#     return wrapper
#
#
# def 时间_时间戳到时间(时间戳):
#     # 时间戳_10位
#     # 需要传入int
#     import time
#     # TODO 长度判断 13位还是10位?正则判断?
#     if len(str(时间戳)) == 13:
#         时间戳 = 时间戳 / 1000
#
#     # return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(时间戳_10位))
#     return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(时间戳))
#
#
# def 时间_取北京时间戳(是否13位=True, 服务器index=0):
#     # 功能:联网 获取北京时间
#
#     # 参数:是否13位  --> 默认13位(毫秒级) 如果为False 则为10位时间戳(秒)
#     # 参数:服务器index -->服务器序号,0是腾讯,1是阿里1688,2是百度,3是腾讯备用服务器
#
#     # Done( 2020年11月20日)
#     # 其实可以优化取北京时间戳  默认选择腾讯,第2次 服务器选择阿里 \
#     #  设置参数"时间服务器序号=0" 可以指定服务器序号
#
#     # TODO 如果实际代码有需求 可以用不同的服务器取2次 时间戳结果的差距 小于5秒即可
#     # TODO 可以判断取到的值 是否准确 可以设定一个时间戳 已经过去的时间 如果<这个时间 也可以报错raise
#     # TODO 如果网页访问失败 可以报错 raise
#
#     # Done 代码:细节1:选择大厂服务器,会更稳定可靠
#     # 解决方案: BATJ
#
#     # Done 代码:细节2:减少网络资源占用
#     # 原因:直接访问它们官方网址 会正常传输网页 有网络资源占用 且耗费时间
#     # 解决方案:访问http地址 因为目前都升级为https 所以会自动重定向 但我们不需要 这里禁止重定向就行了
#
#     # Done 代码:细节3: 减少代码
#     # 原因:不需要解码返回的res,只取响应头中的date就行了,按格式取出来
#
#     # Done 代码细节 响应头Date里面之所以能用文本切片,因为格式固定,且数字字母都是恒定长度:\
#     # 星期固定3位字母,逗号,空格,日固定2位,月份固定3位字母等等.就是数字固定2位 年份固定4位
#     # Date: Thu, 19 Nov 2020 19:55:01 GMT
#
#     # Done 因为时间戳是相对格林威治时间经过的秒数,北京时间有8小时偏移,所以这里要加8*3600秒
#
#     import time
#     import urllib.request
#
#     # 禁止重定向语句  # 这里覆写了urllib.request.HTTPRedirectHandler 里面的302重定向
#     class NoRedirHandler(urllib.request.HTTPRedirectHandler):
#         def http_error_302(self, req, fp, code, msg, headers):
#             return fp
#
#         http_error_301 = http_error_302
#
#     # url 列表:
#     # url = 'https://www.baidu.com'
#     # url = 'http://www.baidu.com/search/error.html'
#     # url = 'http://www.baidu.com'
#     # url = 'http://www.tencent.com'
#     # url = 'http://www.1688.com'
#     # url = 'http://www.qq.com'
#
#     url_list = [
#         'http://www.tencent.com',
#         'http://www.1688.com',
#         'http://www.baidu.com',
#         'http://www.qq.com',
#     ]
#
#     headers = {
#         'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
#     }
#     # 构造request对象  包含:url headers
#     # req = urllib.request.Request(url, headers=headers)
#     req = urllib.request.Request(url_list[服务器index], headers=headers)
#     # opener创建
#     opener = urllib.request.build_opener(NoRedirHandler)  # 这里没用cookies管理 所以只在opener这里添加了覆写的302重定向
#     # opener调用request对象
#     response = opener.open(req)
#     # print(response.read().decode())  #不需要解码返回文本
#     # h = response.info()  # 只需要取出响应头  #也不用 后面直接用  response.headers['date']就可以了
#     # print("响应头", h)
#     # print("Date", h["Date"])
#     t = response.headers['date']
#     # print('Date', t)  # Tue, 24 Sep 2019 16:44:10 GMT
#     # 将日期时间字符转化为gmt_time元组
#     gmt_time = time.strptime(t[5:25], "%d %b %Y %H:%M:%S")  # 截取从日期到秒 不要开头的星期和逗号空格和尾巴的GMT
#     # print("gmt_time", gmt_time)
#     # 将GMT时间转换成北京时间
#     # time.mktime(gmt_time) 把结构化的元组 转为秒数 就是时间戳
#     # time.localtime  把一个时间戳转化为struct_time元组
#     # local_time = time.localtime(time.mktime(gmt_time) + 8 * 3600)
#     # return
#     i = time.mktime(gmt_time) + 8 * 3600
#     return i * 1000 if 是否13位 else i
#     # time.mktime(gmt_time) + 8 * 3600 就是北京时间戳  但是单位是秒
#     # print("local_time", local_time)  # struct_time元组
#
#     # 别人的写法:https://www.jb51.net/article/151823.htm
#     # str1 = "%u-%02u-%02u" % (local_time.tm_year,local_time.tm_mon, local_time.tm_mday)
#     # str2 = "%02u:%02u:%02u" % (local_time.tm_hour, local_time.tm_min, local_time.tm_sec)
#     # cmd = 'date -s "%s %s"' % (str1, str2)
#     # print("cmd", cmd)  #"2019-09-25 02:10:08"
#
#     # 我的写法:
#     # print(time.strftime("%Y-%m-%d %H:%M:%S", local_time))  # 2019-09-25 02:10:08
#     # print(time.strftime("%Y{}%m{}%d{}%H{}%M{}%S{}", local_time).format("年", "月", "日", "时", "分", "秒"))
#     # print(时间_到文本(True, local_time))
#     # return 时间_到文本(True, local_time)
#
#
# def 时间_到文本(时间格式index=0, timetuple=None):
#     """
#     :param 时间格式index:
#     # 0 :  N年N月N日  示例:2020年11月20日
#     # 1 :  N年N月N日N时N分N秒  示例:2020年11月20日4时25分38秒
#     # 2 :  N年N月N日 N时N分N秒  示例:2020年11月20日 4时25分38秒
#     # 3 :  年-月-日 时:分:秒  2020-11-20 4:25:38
#     # 4 :  年/月/日 时/分/秒  2020/11/20 4/25/38
#     :param timetuple:
#         # 可传入 时间元组  如果不传 就默认取现行时间
#     :return:
#     """
#     # Done (2020年11月20日) 在版本3基础上 添加功能:时间格式 如果后续有需要 直接去list中添加对应格式
#     # 时间格式index= ?
#     # 0 :  N年N月N日  示例:2020年11月20日
#     # 1 :  N年N月N日N时N分N秒  示例:2020年11月20日4时25分38秒
#     # 2 :  N年N月N日 N时N分N秒  示例:2020年11月20日 4时25分38秒
#     # 3 :  年-月-日 时:分:秒  2020-11-20 4:25:38
#     # 4 :  年/月/日 时/分/秒  2020/11/20 4/25/38
#
#     # def 时间_到文本(包含时分秒=False, timetuple=None):
#     # 在版本2基础上 添加功能:支持传入 时间元组  如果不传 就默认取现行时间
#     # struct_time  一般由time.localtime([secs])生成 参数secs省略就是取现行时间戳time.time()
#     # struct_time 被提示重名了 改成了 timetuple
#
#     import time
#     # 检查到默认时间元组为None,那么就是取现行时间      # 如果没传入时间元组 就代表取现行时间
#     if timetuple is None:
#         timetuple = time.localtime()
#     # time.struct_time(tm_year=2019, tm_mon=9, tm_mday=16, tm_hour=23, tm_min=45, tm_sec=13, tm_wday=0, tm_yday=259, tm_isdst=0)
#
#     # 用*打散列表/元组等有序合集即可,需要几个参数它自己会传入个数,不会报错
#     # N年N月N日 N时N分N秒  1=年-月-日 时:分:秒  2=年/月/日 时/分/秒  3=年月日时分秒
#     # 时间格式index
#     # 0 :  N年N月N日  示例:2020年11月20日
#     # 1 :  N年N月N日N时N分N秒  示例:2020年11月20日4时25分38秒
#     # 2 :  N年N月N日 N时N分N秒  示例:2020年11月20日 4时25分38秒
#     # 3 :  年-月-日 时:分:秒  2020-11-20 4:25:38
#     # 4 :  年/月/日 时/分/秒  2020/11/20 4/25/38
#     result_list = [
#         "{}年{}月{}日",
#         "{}年{}月{}日{}时{}分{}秒",
#         "{}年{}月{}日 {}时{}分{}秒",
#         "{}-{}-{} {}:{}:{}",
#         "{}/{}/{} {}/{}/{}",
#     ]
#
#     return result_list[时间格式index].format(*timetuple)
#
#     # 历史写法3
#     # """
#     # if 包含时分秒:
#     #     result = "{}年{}月{}日{}时{}分{}秒"
#     # else:
#     #     result = "{}年{}月{}日"
#     # return result.format(*timetuple)
#     # """
#
#     # 历史写法3:
#     # """
#     # if 包含时分秒:
#     #     result = "{}年{}月{}日{}时{}分{}秒".format(*timetuple)
#     # else:
#     #     result = "{}年{}月{}日".format(*timetuple)
#     # return result
#     # """
#
#     # 历史写法:
#     # """
#     # # get 取出 指定n位 年/月/日/时/分/秒 组合 //3位就是年月日,6位就是时分秒  #自己根据需要组合长度 1~6位
#     # # 这里def 用到了变量struct_time 因此取到的起码不是None 要么是传进来的时间元组 要么是现行时间元组
#     # def _get(n, timetuple=timetuple):
#     #     # time.struct_time(tm_year=2019, tm_mon=9, tm_mday=16, tm_hour=23, tm_min=45, tm_sec=13, tm_wday=0, tm_yday=259, tm_isdst=0)
#     #     # print(t[0]) #2019  #这种居然可行  它就是个元组方式的数据  但是注意它是int型
#     #     # ★下面的意思是 按 2019 年 9 月 16 日 23 时 45 分 13 秒 顺序将这些文本添加进数组 再连接起来
#     #     s = '年月日时分秒'  # list=["年","月","日"]  str也可以类似for循环进行遍历和取成员
#     #     lis = []
#     #     for i in range(n):
#     #         lis.append(str(timetuple[i]))  # 整数int 转为文本型
#     #         lis.append(s[i])
#     #     return ''.join(lis)  # 使用列表join而不是str1+str的方式是因为好像每次+都要生成一个新的str 而将list进行join会一次性申请内存空间,更省资源
#     #
#     # return _get(6) if 包含时分秒 else _get(3)
#     # """
#
#
# def 时间_设置电脑时间_北京时间(服务器index=0):
#     # 设置电脑时间 为 北京时间  时间服务器为腾讯服务器
#     # 参数:服务器index -->服务器序号,0是腾讯,1是阿里1688,2是百度,3是腾讯备用服务器
#
#     import time
#     import os
#
#     t = time.localtime(时间_取北京时间戳(是否13位=False, 服务器index=服务器index))  # 10位时间戳 转换为 时间 元组形式
#     print(t)  # time.struct_time(tm_year=2020, tm_mon=11, tm_mday=20, tm_hour=3, tm_min=0, tm_sec=28, tm_wday=4, tm_yday=325, tm_isdst=0)
#
#     # li =list(t)[:6]  # 把元组转换成列表 list(t)  # 切片保留0~5  切片实际规则[begin=0:end=xxx)
#     # cmd = r"date {}/{}/{}& time {}:{}:{}".format(*li)
#     cmd = r"date {}/{}/{}& time {}:{}:{}".format(*t)
#
#     # cmd = r"date 2015/11/25& time 11:15:00".format(t)
#     # date xxx 和 time xxx 命令分别是修改日期 修改时间  # cmd命令中可以用&连接起来
#     # 6个参数 用*打散放入这里  -->实际测试不用转换成列表再打散 元组直接可以打散参数的合集
#
#     # r = os.popen(cmd)
#     # print(r.read)  #: <built-in method read of _io.TextIOWrapper object at 0x0267BF30>
#     os.popen(cmd)
#
#
# # 在版本2基础上 添加功能:支持传入 时间元组  如果不传 就默认取现行时间
# # struct_time  一般由time.localtime([secs])生成 参数secs省略就是取现行时间戳time.time()
# # struct_time 被提示重名了 改成了 timetuple
# def 时间_到文本_____(包含时分秒=False, timetuple=None):
#     """
#      #使用示例:
#      >>> 时间_到文本_____(包含时分秒=False)
#      '2020年11月28日'
#      >>> if None:print("其它测试")
#      >>> '时' in str(时间_到文本_____(包含时分秒=True))  #测试是否含有关键字 '秒'
#      True
#      >>> '分' in str(时间_到文本_____(包含时分秒=True))  #测试是否含有关键字 '秒'
#      True
#      >>> '秒' in str(时间_到文本_____(包含时分秒=True))  #测试是否含有关键字 '秒'
#      True
#      """
#     import time
#     # 检查到默认时间元组为None,那么就是取现行时间      # 如果没传入时间元组 就代表取现行时间
#     if timetuple is None:
#         timetuple = time.localtime()
#
#     # get 取出 指定n位 年/月/日/时/分/秒 组合 //3位就是年月日,6位就是时分秒  #自己根据需要组合长度 1~6位
#     # 这里def 用到了变量struct_time 因此取到的起码不是None 要么是传进来的时间元组 要么是现行时间元组
#     def _get(n, timetuple=timetuple):
#         # time.struct_time(tm_year=2019, tm_mon=9, tm_mday=16, tm_hour=23, tm_min=45, tm_sec=13, tm_wday=0, tm_yday=259, tm_isdst=0)
#         # print(t[0]) #2019  #这种居然可行  它就是个元组方式的数据  但是注意它是int型
#         # ★下面的意思是 按 2019 年 9 月 16 日 23 时 45 分 13 秒 顺序将这些文本添加进数组 再连接起来
#         s = '年月日时分秒'  # list=["年","月","日"]  str也可以类似for循环进行遍历和取成员
#         lis = []
#         for i in range(n):
#             lis.append(str(timetuple[i]))  # 整数int 转为文本型
#             lis.append(s[i])
#         return ''.join(lis)  # 使用列表join而不是str1+str的方式是因为好像每次+都要生成一个新的str 而将list进行join会一次性申请内存空间,更省资源
#
#     return _get(6) if 包含时分秒 else _get(3)
#
#
# def 时间_取现行时间戳():  # 这个写13位  #int型
#     # 使用示例   >>> 时间_取现行时间戳()  # todo这个没办法直接测试啊  '1234567890123'
#     """
#     >>> len(str(时间_取现行时间戳()))==13   #测试是否13位
#     True
#     >>> 时间_取现行时间戳() > 1569086434031  #2019年9月21日某个时间戳
#     True
#     """
#     import time
#     return int(round(time.time() * 1000))  # return x 不用加括号 不用写成return (x)
#
#
# # 版本: 直接调用: 时间_取北京时间戳()  时间_到文本()
# def 时间_取北京时间(服务器index=0):
#     import time
#     # t = time.localtime(时间_取北京时间戳(是否13位=False))  # 10位时间戳 转换为 结构化时间 元组形式
#     t = time.localtime(时间_取北京时间戳(是否13位=False, 服务器index=服务器index))  # 10位时间戳 转换为 时间 元组形式
#
#     # return 时间_到文本(包含时分秒=True, timetuple=t)  # 时间元组 转换:格式:xx年x月x日x时x分x秒
#     return 时间_到文本(时间格式index=1, timetuple=t)  # 时间元组 转换:格式:xx年x月x日x时x分x秒
#
#
# def 时间_取北京时间戳____(是否13位=True):
#     # 默认13位
#     # 联网 获取北京时间
#     import time
#     import urllib.request
#
#     # 禁止重定向语句  # 这里覆写了urllib.request.HTTPRedirectHandler 里面的302重定向
#     class NoRedirHandler(urllib.request.HTTPRedirectHandler):
#         def http_error_302(self, req, fp, code, msg, headers):
#             return fp
#
#         http_error_301 = http_error_302
#
#     # url 列表:
#     # url = 'https://www.baidu.com'
#     # url = 'http://www.baidu.com/search/error.html'
#     # url = 'http://www.baidu.com'
#     # url = 'http://www.tencent.com'
#     # url = 'http://www.1688.com'
#     url = 'http://www.qq.com'
#     headers = {
#         'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
#     }
#     # 构造request对象  包含:url headers
#     req = urllib.request.Request(url, headers=headers)
#     # opener创建
#     opener = urllib.request.build_opener(NoRedirHandler)  # 这里没用cookies管理 所以只在opener这里添加了覆写的302重定向
#     # opener调用request对象
#     response = opener.open(req)
#     # print(response.read().decode())  #不需要解码返回文本
#     # h = response.info()  # 只需要取出响应头  #也不用 后面直接用  response.headers['date']就可以了
#     # print("响应头", h)
#     # print("Date", h["Date"])
#     t = response.headers['date']
#     # print('Date', t)  # Tue, 24 Sep 2019 16:44:10 GMT
#     # 将日期时间字符转化为gmt_time元组
#     gmt_time = time.strptime(t[5:25], "%d %b %Y %H:%M:%S")  # 截取从日期到秒 不要开头的星期和逗号空格和尾巴的GMT
#     # print("gmt_time", gmt_time)
#     # 将GMT时间转换成北京时间
#     # time.mktime(gmt_time) 把结构化的元组 转为秒数 就是时间戳
#     # time.localtime  把一个时间戳转化为struct_time元组
#     # local_time = time.localtime(time.mktime(gmt_time) + 8 * 3600)
#     # return
#     i = time.mktime(gmt_time) + 8 * 3600
#     return i * 1000 if 是否13位 else i
#     # time.mktime(gmt_time) + 8 * 3600 就是北京时间戳  但是单位是秒
#     # print("local_time", local_time)  # struct_time元组
#
#     # 别人的写法:https://www.jb51.net/article/151823.htm
#     # str1 = "%u-%02u-%02u" % (local_time.tm_year,local_time.tm_mon, local_time.tm_mday)
#     # str2 = "%02u:%02u:%02u" % (local_time.tm_hour, local_time.tm_min, local_time.tm_sec)
#     # cmd = 'date -s "%s %s"' % (str1, str2)
#     # print("cmd", cmd)  #"2019-09-25 02:10:08"
#
#     # 我的写法:
#     # print(time.strftime("%Y-%m-%d %H:%M:%S", local_time))  # 2019-09-25 02:10:08
#     # print(time.strftime("%Y{}%m{}%d{}%H{}%M{}%S{}", local_time).format("年", "月", "日", "时", "分", "秒"))
#     # print(时间_到文本(True, local_time))
#     # return 时间_到文本(True, local_time)
#
#
# def test_时间_取北京时间():
#     print(时间_取北京时间())
#
#
# def 文件_图片写到文件(file, data):
#     import os
#     file = os.path.realpath(file)  # 1. 转换为绝对路径  相对路径用下面的方法是取不到目录的
#     file_dir = os.path.dirname(file)  # 2. 取目录 用于:检查文件多级目录是否存在  # 2.1 dir会与内置方法dir()重名 会导致内置方法无效  这里用file_dir
#     if not os.path.isdir(file_dir): os.makedirs(file_dir)  # 3. 检查文件多级目录是否存在,如果不存在则创建目录
#
#     # 多用于 图片字节集 写到本地图片
#     with open(file, "wb") as f:
#         f.write(data)
#
#
# def list_去重复_找重复(lis):
#     重复元素_list = []
#     new_list = []
#     for i in lis:
#         if i not in new_list:
#             new_list.append(i)
#         else:
#             # 重复元素_list.append(i)  # 写法1 这种写法 会导致 重复的元素 会重复添加进 如果不想这么重复 可以判断是否在 重复元素_list
#             if i not in 重复元素_list: 重复元素_list.append(i)  # 写法2: 这种重复的元素 不会重复添加进来
#
#     return new_list, 重复元素_list
#
#
# def 文本_子文本替换(string, old, new, *count):
#     # string=''
#     return string.replace(old, new, *count)  # replace 不会改变原 string 的内容。 需要接收方 接收新的值
#
#
# # 文本_读入文本   #一.文件不存在   二.文件编码是gbk /文件编码是utf8
# def 文件_读入文本(file):
#     try:
#         with open(file, mode="r", encoding='utf-8') as f:
#             return f.read()
#     except UnicodeDecodeError:
#         # print('检测到编码可能是gbk,正在调用gbk...请稍候...')
#         with open(file, mode="r", encoding='gbk') as f:
#             return f.read()
#
#
# def 文件_是否存在(path):
#     import os
#     return os.path.isfile(path)  # 这里需要是绝对路径 相对路径无法判断 -->3.6版本好像可以接受相对路径
#
#
# def 文件_取运行目录():
#     import os
#     return os.getcwd()  # 当前xx.py文件的目录
#
#
# def 文件夹_是否存在(path):
#     import os
#     return os.path.isdir(path)
#
#
# def 文件夹_创建(path):
#     import os
#     if not os.path.isdir(path):  # 文件夹不存在
#         os.makedirs(path)  # 文件夹 创建
#     # 调试版:↓↓↓
#     # if os.path.isdir(path):
#     #     print(path,"已经存在")
#     # else:
#     #     print(path,"不存在,即将创建")
#     #     os.makedirs(path)
#
#
# def 文件_是否存在___废弃(file, 只判断文件=True):
#     # ■废弃原因:因为  os.path.isfile 直接可以判断 同时 文件夹 是否存在做了另外个函数
#
#     # import pathlib
#     # return pathlib.Path(file).is_file()
#     # 方法1:
#     # import pathlib
#     # print(pathlib.Path(file).exists())  # 无论是文件还是文件夹 存在 就存在
#     # print(pathlib.Path(file).is_file())  # 如果没有这个文件,哪怕是同名文件夹 也不行
#     # 方法2:
#     # import os
#     # print(os.path.exists(file))  # 无论是文件还是文件夹 存在 就存在
#     # print(os.path.isfile(file))  # 如果没有这个文件,哪怕是同名文件夹 也不行
#     import os
#     if 只判断文件:
#         return os.path.isfile(file)  # 只判断文件
#     else:
#         return os.path.exists(file)  # 该路径只要存在,无论是文件还是文件夹,都可以
#
#
# def 文件路径_取_名称_后缀(path):
#     # ■后缀格式如".py" ".txt" 包含"."符号
#     import os
#     # ■这里无法分离相对路径的 需要转换为绝对路径
#     path = os.path.realpath(path)  # 转换为绝对路径
#     path_dir, path_fname = os.path.split(path)  # 取文件夹名和文件名
#     filename, extension = os.path.splitext(path_fname)  # 取文件名前面和后缀
#     return filename, extension
#
#
# def 文件路径_取_目录_文件名(path):
#     import os
#     # ■这里无法分离相对路径的 需要转换为绝对路径
#     path = os.path.realpath(path)  # 转换为绝对路径
#     path_dir, path_fname = os.path.split(path)
#     return path_dir, path_fname
#
#
# def 文件路径_取目录(path):
#     import os
#     return os.path.dirname(os.path.realpath(path))
#
#
# def 文件路径_取文件名(path):
#     import os
#     return os.path.basename(os.path.realpath(path))
#
#
# def 文件_更名(file_oldname, file_newname):
#     # os.renames(old, new)
#     import os
#     # todo 需要判断文件是否存在吗??
#     # os.rename(old_file_path, new_file_path), 只能对相应的文件进行重命名, 不能重命名文件的上级目录名.
#     # os.renames(old_file_path, new_file_path), 是os.rename的升级版, 既可以重命名文件, 也可以重命名文件的上级目录名
#     os.renames(file_oldname, file_newname)
#
#
# def 文件_移动(old, new):
#     import os
#     import shutil
#     # shutil.move(old, new)  # 移动文件  基本写法
#
#     # 1. old文件要存在
#     # 2. new文件所在文件夹要存在
#     # TODO 3. 如果new文件已经 存在 如何处理? 覆盖? shutil.move 是会覆盖的
#     if not os.path.isfile(old):
#         print(old, "not exist!")
#     else:
#         new_dir, new_filename = os.path.split(new)  # 分离目标路径的 文件夹和文件名
#         if not os.path.isdir(new_dir):  # 如果 目标文件夹 不存在
#             print(new_dir, "not exist!")
#             os.makedirs(new_dir)  # 创建 文件夹
#         shutil.move(old, new)  # 移动 文件
#         print("文件_移动  {} -> {}".format(old, new))
#
#
# def 文本_写到文件(file, text):
#     # 覆盖式写入
#     import os
#     file = os.path.realpath(file)  # 1. 转换为绝对路径  相对路径用下面的方法是取不到目录的
#     file_dir = os.path.dirname(file)  # 2. 取目录 用于:检查文件多级目录是否存在  # 2.1 dir会与内置方法dir()重名 会导致内置方法无效  这里用file_dir
#     if not os.path.isdir(file_dir): os.makedirs(file_dir)  # 3. 检查文件多级目录是否存在,如果不存在则创建目录
#
#     with open(file, 'w', encoding='utf-8') as f:
#         f.write(text)
#
#
# # 文本_追加文本  #往文件 追加 不是覆写  可选参数:结尾是否添加换行符 默认为真
# def 文本_追加文本(file, data, mode=True):
#     """
#     file:文件路径
#     data:追加的数据
#     mode:结尾是否增加换行,默认为假 -->改为默认为真
#     """
#
#     import os
#     file = os.path.realpath(file)  # 1. 转换为绝对路径  相对路径用下面的方法是取不到目录的
#     file_dir = os.path.dirname(file)  # 2. 取目录 用于:检查文件多级目录是否存在  # 2.1 dir会与内置方法dir()重名 会导致内置方法无效  这里用file_dir
#     if not os.path.isdir(file_dir): os.makedirs(file_dir)  # 3. 检查文件多级目录是否存在,如果不存在则创建目录
#
#     # 追加方式  "a+" 打开文件
#     with open(file, mode="a+", encoding='utf-8') as f:
#         # 如果模式==True 添加自动换行  模式==False 直接追加文本
#         f.write(data + '\n') if mode else f.write(data)
#
#
# def 文本_取中间文本(string, front, behind):
#     # 返回值:None 或者 符合条件的string
#
#     front_pos = string.find(front)
#
#     if front_pos == -1:
#         return None
#
#     start_pos = front_pos + len(front)  # 修改 find文本 起始位置
#
#     behind_pos = string.find(behind, start_pos)
#
#     if behind_pos == -1:
#         return None
#
#     return string[start_pos:behind_pos]
#
#
# def 文本_取中间_批量(string, front, behind):
#     # 返回值 : [] 或 [string1,string2,...]
#     # 示例:文本_取中间_批量('0123450123445','23','5') -->> ['4','44']
#     # 示例:文本_取中间_批量('0123450123445','236','5') -->>[]
#
#     lis = []
#
#     start_pos = 0
#     while True:
#         front_pos = string.find(front, start_pos)
#
#         if front_pos == -1:
#             break
#
#         start_pos = front_pos + len(front)  # 修改 find文本 起始位置
#
#         behind_pos = string.find(behind, start_pos)
#
#         if behind_pos == -1:
#             break
#
#         lis.append(string[start_pos:behind_pos])  # 加入列表
#
#         start_pos = behind_pos + len(behind)  # 修改 find文本 起始位置 为 后面文本的下一个
#
#     return lis
#
#
# # 正则  #文本_取中间文本   文本_取中间文本
# def 文本_取中间文本_正则_(string, front, behind):
#     # ■□2020年10月20日更新: 涉及元字符转义 不推荐
#     # def 文本_取中间文本(string, front, behind, 标识自动转义=False):
#     # 返回值:None 或者 str1
#     # 示例1:文本_取中间文本('0123450123445','23','5') -->> '4'
#     # 示例1:文本_取中间_批量('0123450123445','236','5') -->>None
#     import re
#     # search 只查1次  #符合条件就停止
#     # re.search(正则表达式,string,re.S)会返回一个对象,然后对该对象使用.group(i)方法  #备注:这里是因为正则有分组(.*?) 所以才是.group(1)
#     # print(re.search(front + '(.*?)' + behind, string, re.S))
#     # print(re.search(front + '(.*?)' + behind, string, re.S).group(0))
#     # return re.search(front + '(.*?)' + behind, string, re.S).group(1)   #■★bug:当无匹配时,返回值None是没有group方法的
#
#     # front和behind 里面如果有元字符 比如() 就需要处理 否则影响正则表达式 导致取出None
#     '''
#     if 标识自动转义:
#         for i in ".*?()[]":
#             if i in front:         front = re.sub('[{}]'.format(i), "\\" + i, front)
#             if i in behind:        behind = re.sub('[{}]'.format(i), "\\" + i, behind)
#             # front = re.sub('[%s]' % i, "\\" + i, front)
#             # behind = re.sub('[%s]' % i, "\\" + i, behind)
#             # 原先问题:不去判断 正则直接替换的话 会报错 : FutureWarning: Possible nested set at position 1
#     '''
#     for i in ".*?()[]+-":  # TODO 可能还有问题 因为元字符 还包括 xxxxxxxxxxx 等等
#         # front = front.replace(i, "\\" + i)
#         # behind = behind.replace(i, "\\" + i)
#         if i in front:          front = front.replace(i, "\\" + i)
#         if i in behind:         behind = behind.replace(i, "\\" + i)
#         # 【知识点:】如果不判断是否存在 直接使用替换时, replace方式 都不会报错
#     #  ■ 之所以要转义  是因为比如 (121977522)要取(和)之间的文本 使用front + '(.*?)' + behind就出错了
#
#     r = re.search(front + '(.*?)' + behind, string, re.S)
#     return r.group(1) if r else None  # 问题:这里是否要改成""? 因为很多时候 是str1+str2+..这种组合来的?
#     # return r.group(1) if r else r   #因为当r为None时 return r 等同于None
#
#
# # 文本_取中间_批量   #正则
# def 文本_取中间_批量_正则_(string, front, behind):
#     # ■□2020年10月20日更新: 涉及元字符转义 不推荐
#     # def 文本_取中间_批量(string, front, behind, 标识自动转义=False):
#     # 返回值:[] 或者 [str1,str2,...]
#     # 示例1:文本_取中间_批量('0123450123445','23','5') -->> ['4','44']
#     # 示例1:文本_取中间_批量('0123450123445','236','5') -->>[]
#     """
#     >>> 文本_取中间_批量('0123450123445','23','5')
#     ['4', '44']
#     >>> 文本_取中间_批量('0123450123445','236','5')
#     []
#     """
#     import re
#
#     # front和behind 里面如果有元字符 比如() 就需要处理 否则影响正则表达式 导致取出None
#     '''
#     if 标识自动转义:
#         for i in ".*?()[]":
#             if i in front:         front = re.sub('[{}]'.format(i), "\\" + i, front)
#             if i in behind:        behind = re.sub('[{}]'.format(i), "\\" + i, behind)
#             # front = re.sub('[%s]' % i, "\\" + i, front)
#             # behind = re.sub('[%s]' % i, "\\" + i, behind)
#             # 原先问题:不去判断 正则直接替换的话 会报错 : FutureWarning: Possible nested set at position 1
#     '''
#
#     for i in ".*?()[]":  # TODO 可能还有问题 因为元字符 还包括 + - \ ^ { } 等等
#         # front = front.replace(i, "\\" + i)
#         # behind = behind.replace(i, "\\" + i)
#         if i in front:          front = front.replace(i, "\\" + i)
#         if i in behind:         behind = behind.replace(i, "\\" + i)
#         # 【知识点:】如果不判断是否存在 直接使用替换时, replace方式 都不会报错
#
#     # re.S 表示“.”（不包含外侧双引号，下同）的作用扩展到整个字符串，包括“\n”
#     return re.findall(front + '(.*?)' + behind, string, re.S)
#
#
# # 检验是否含有中文字符
# def 文本_是否包含汉字(string):
#     """
#     >>> 文本_是否包含汉字('123ni你好asasa')
#     True
#     >>> 文本_是否包含汉字('123niasasa')
#     False
#     >>> 文本_是否包含汉字('123')
#     False
#     >>> 文本_是否包含汉字('a')
#     False
#     >>> 文本_是否包含汉字('你')
#     True
#     >>> 文本_是否包含汉字('1')
#     False
#     """
#     for i in string:
#         if '\u4e00' <= i <= '\u9fa5':
#             # if '一' <= i <= '龥':
#             return True
#     # 循环完毕 都还没返回 那结果就是False了
#     return False
#
#
# def 文本_取汉字(string):
#     # 返回:列表  空列表[]  或者 有数据的列表
#     # Failed example:    文本_取汉字('能取group取值')
#     # Expected:    ['能取','取值']
#     # Got: ['能取', '取值']
#     #     >>> if None:print('代码示例:')
#     """
#     >>> 文本_取汉字('你好gro哈哈up呵呵')
#     ['你好', '哈哈', '呵呵']
#     >>> 文本_取汉字('123aaaa121212')   #测试
#     []
#     # >>> if False:print("其他测试用例:--------------------------+----------------------------")
#     >>> 文本_取汉字('你123a你好吗aaa文本')
#     ['你', '你好吗', '文本']
#     >>> 文本_取汉字('1')
#     []
#     >>> 文本_取汉字('a')
#     []
#     """
#     import re
#     # return re.compile("[\u4e00-\u9fa5]").findall(文本)
#     return re.compile("[\u4e00-\u9fa5]+").findall(string)  # 备注:这种是返回列表  并且没有re.S注释掉换行符
#     # search的问题:需要对re.search返回的对象进行判断,不是None才能取group取值.
#     # return re.compile("[\u4e00-\u9fa5]+",re.S).search(string).group()   #这种是返回单条数据 并且注释掉换行符 要对其对象是否None判断后 再对其group取值
#     # return re.compile("[\u4e00-\u9fa5]+",re.S).search(string).group()   #这种是返回单条数据 并且注释掉换行符 要对其对象是否None判断后 再对其group取值
#     # return re.search("[\u4e00-\u9fa5]+",string,re.S).group()   #这种是返回单条数据对象 并且注释掉换行符 要对其对象是否None判断后 再对其group取值
#
#
# def 文本_取英文数字(string):
#     # 返回: 列表  空列表[]  或者 有数据的列表
#     import re
#     return re.compile("[a-zA-Z0-9]+").findall(string)  # 连在一起的会一起加入列表  #没有+号 会返回1个个的匹配对象
#
#
# def 文本_取数字(string):
#     # 返回列表  空列表[]  或者 有数据的列表
#     """
#     >>> 文本_取数字('00abbbb12你3334好013549abcde')
#     ['00', '12', '3334', '013549']
#     >>> 文本_取数字('accva')
#     []
#     """
#     import re
#     # return re.compile("[0-9]").findall(文本)  #这种会返回1个个的数字
#     return re.compile("[0-9]+").findall(string)  # 连在一起的数字会一起加入列表  #可行
#     # return re.compile("\d+").findall(string)  #连在一起的数字会一起加入列表 #这个也行  \d和\\d都可以
#
#
# def 数组_到文本(数组, 连接符=''):  # python里面直接是 join
#     # 原本是list 但是内置list()方法 会导致list()失效
#     return 连接符.join(数组)
#
#
# # ★ js计算()  '09 python_执行js语句_execjs_0笔记demo.py'
# # ★ 因为安装了node.js 所以目前引擎默认是Node.js (V8),有部分js使用Node.js (V8)会报错,异常.因此出现异常则切换到JScript.使用完毕就切换回来Node.js (V8)
# # ★ 至于为什么不直接使用JScript,是因为JScript有时候计算的特别慢.
# def js计算(file, *args):
#     # 格式:js计算(js文件路径,js中func名称,func要用的参数)
#     # 示例1:js计算('js_2.js','get', '134854280','ZUdXWHpXUFNEQUdUTWdKeg==')      #js文件 相对路径 就在本目录下
#     # 示例2:js计算(r'c:\js_2.js','get', '134854280','ZUdXWHpXUFNEQUdUTWdKeg==')  #js文件完整路径
#     """
#     简化成一句话代码:
#     """
#     import execjs
#     import os
#     # print('args',args)
#     # print('*args', *args)   # 我的 笔记 :*的作用:uppack  如果不加* 那传进来就是个tuple
#     defult = execjs.get().name  # 取默认js环境  #原因:这里面改到JScript默认就一直是了 不会换回默认环境 因此在切换后 最好置回默认环境
#     # 当然 也可以只使用JScript环境
#
#     file = 文件_读入文本(file)  # ★这个有自动适配gb2312或者utf-8
#     # with open(file, mode="r", encoding='utf-8') as f:
#     #     file = f.read()
#
#     try:
#         # res = execjs.compile(open('js_2.js', 'r', encoding='utf8').read()).call('get', '134854280','ZUdXWHpXUFNEQUdUTWdKeg==')
#         print(execjs.get().name, '默认js')
#         res = execjs.compile(file).call(*args)
#         # res = execjs.compile(file).call(args,)
#         # 我的笔记:这种就是错误的写法 原因是没有*,会传入tuple,而非单独的每个参数
#     except Exception:  # except:
#         print(execjs.get().name, '检测到默认js存在问题,已切换至JScript')
#         os.environ["EXECJS_RUNTIME"] = "JScript"
#         res = execjs.compile(file).call(*args)
#         os.environ["EXECJS_RUNTIME"] = defult  # 置回默认js环境
#
#     return res
#
#
# def 时间_取月总天数(year=None, month=None):
#     import calendar
#     if year is None and month is None:
#         import time
#         t = time.localtime()  # 当前时间
#         year = t.tm_year
#         month = t.tm_mon
#     return calendar.monthrange(year, month)[1]
#
#
# '''
# def 时间_是否本月末():
#     import datetime
#     import calendar
#     # https://blog.csdn.net/zhaojikun521521/article/details/83054367
#     # 年
#     # 月
#     now = datetime.datetime.now()  # 当前时间
#     y = now.year
#     m = now.month
#     d = now.day
#     d_Last = calendar.monthrange(y, m)[1]  # 取 本月 总天数
#     # d_Last = 时间_取月总天数(y, m)[1]
#     # print(y,m,d,d_Last) #2019 4 30 30
#     return d == d_Last  # return 后面不需要写括号 比如 return (d == d_Last)
# '''
#
#
# def 时间_是否本月末():
#     # 这里要改成 今天 是否月末的真实结果
#     """
#     >>> 时间_是否本月末()
#     False
#     """
#     import time
#     import calendar
#     t = time.localtime()  # 当前时间
#     # y = now.tm_year
#     # m = now.tm_mon
#     # d = t.tm_mday
#     # d = calendar.monthrange(t.tm_year, t.tm_mon)[1]  # 取 该月 总天数
#     # print(calendar.monthrange(y, m))
#     # 第一个元素，这个月的第1天是星期几；  mon~sun  0~6
#     # 第二个元素，这个月的天数；
#     # d_Last = 时间_取月总天数(y, m)[1]
#     # print(y,m,d,d_Last) #2019 4 30 30
#     # return 后面不需要写括号 比如 return (d == d_Last)
#     return t.tm_mday == calendar.monthrange(t.tm_year, t.tm_mon)[1]
#
#
# def 时间_取星期几():
#     # tod  #参考下易语言的写法
#     # 返回  "星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"
#     # 0~6是星期一到日
#     """
#     >>> 时间_取星期几()
#     '星期六'
#     """
#     # 这里需要自己改成今天的真实星期
#
#     import time
#     # 写法1:
#     lis = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
#     return lis[time.localtime().tm_wday]
#     # 写法 1.5:
#     # return ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][time.localtime().tm_wday] #这种就一行搞定了
#     # 写法2:
#     # string = "一二三四五六日"
#     # return "星期" + string [time.localtime().tm_wday]
#     # 写法 2.5:
#     #  return "星期" +  "一二三四五六日"[time.localtime().tm_wday]  #这种就一行搞定了
#
#
# # 这个就是练手  表驱动法 替代大量的if else 见:易语言 精易模块的 时间_取节气文本
# def 时间_取节气文本(i):
#     # 1到24节气
#     """
#     >>> 时间_取节气文本(20)
#     '小雪'
#     """
#     s = "立春,雨水,惊蛰,春分,清明,谷雨;立夏,小满,芒种,夏至,小暑,大暑；立秋,处暑,白露,秋分,寒露,霜降；立冬,小雪,大雪,冬至,小寒,大寒"
#     # print(len("立春"))  2
#     # print(len(","))    1
#     # print(len("；"))   1 这种全角符号也是占位1 好评
#     # print(len(s))  #71 因为尾部结束再没有,了 只有2位 但是不影响切片 切片不会过界 就算过界只取到结尾
#     # i=i-1  #因为是 1~24节气 对应 0~23
#     # i=i*3   #因为按这种文本格式 每3位一组 所以切片开头就是i*3 因为包头不包尾 长度为2 就i : i+2
#     i = (i - 1) * 3
#     return s[i:i + 2]
#
#
# def test_时间_取节气文本():
#     for i in range(1, 25):  # 这里要写1到24节气 就得这么写 不能从0开始 从0开始就到-1了 那个里面
#         print(i, 时间_取节气文本(i))
#
#
# def json_加载(s):
#     import json
#     #
#     try:
#         s = json.loads(s)
#     except Exception:
#         # print('直接进行json.loads(),捕捉到报错,重新进行json.dumps(),json.loads()进行加载')
#         s = json.dumps(s)
#         s = json.loads(s)
#     # 返回json对象
#     return s
#
#
# # logging 模块 打包一个方法
# def loggerNew_____(filename=None, 输出到屏幕=True):  # ■□这种不是单例模式  2020年11月写了个单例模式的 在模块liukai_single_log
#     # def _logger(filename=None, 输出到屏幕=True):
#     """用法示例:
#     #1.获取一个初始化对象:
#         logger = _logger()    #默认  :日志路径:./MyLog/Log 文件
#         logger = _logger(输出到屏幕=False)  #这种就不会输出到屏幕上 只会写日志
#         logger = _logger(filename="my_test_logging")  #这种日志路径./MyLog/my_test_logging文件
#     #2.调用:
#         logger.warning("开始...")
#         logger.info("提示")
#         logger.error("错误")
#         logger.debug("查错")
#     """
#     import os
#     import logging.handlers
#     #    from logging import handlers
#
#     # 初始赋值:filename
#     if filename is None:
#         filename = 'Log'
#
#     # 创建log对象
#     logger = logging.getLogger(filename)  # logger = logging.getLogger()也可以 对应的是Formatter里面的name
#     # 设置日志等级
#     logger.setLevel(logging.DEBUG)
#     # logger.setLevel(logging.ERROR)
#     # 日志格式
#     formatter = logging.Formatter('%(asctime)s - [%(filename)s] - [Line:%(lineno)d] - [%(levelname)s] - %(message)s')
#     # formatter = logging.Formatter('[%(asctime)s] - [%(filename)s] - [Line:%(lineno)d] - [%(levelname)s] - %(message)s')
#     # formatter = logging.Formatter('[%(asctime)s] - %(filename)s [Line:%(lineno)d] - [%(levelname)s]-[thread:%(thread)s]-[process:%(process)s] - %(message)s')
#     # formatter = logging.Formatter(fmt="%(asctime)s %(name)s %(filename)s %(message)s", datefmt="%Y/%m/%d %X")
#     # 创建:写日志文件的句柄
#     os.makedirs("./MyLog/", exist_ok=True)  # 创建文件夹
#     fh = logging.handlers.TimedRotatingFileHandler(filename="./MyLog/" + filename, when='MIDNIGHT', interval=1,
#                                                    backupCount=0, encoding="utf-8")
#     # 设置滚动日志的后缀
#     fh.suffix = "%Y-%m-%d.log"
#     # 绑定日志格式到句柄
#     fh.setFormatter(formatter)
#     # 每个句柄单独设置级别
#     # fh.setLevel(logging.DEBUG)
#     # 句柄 添加到logger对象
#     logger.addHandler(fh)
#
#     """判断是否输出到屏幕"""  # 创建输出到屏幕句柄
#     if 输出到屏幕:
#         ch = logging.StreamHandler()
#         ch.setFormatter(formatter)
#         # ch.setLevel(logging.DEBUG)  #每个句柄单独设置级别
#         logger.addHandler(ch)
#
#     return logger
#
#
# # 线程_启动  线程方式运行 子程序
# def thread_it(func, *args, **kwargs):
#     import threading
#     '''将函数打包进线程'''
#     # 创建
#     t = threading.Thread(target=func, args=args, kwargs=kwargs)
#     # 守护 !!!
#     t.setDaemon(True)
#     # 启动
#     t.start()
#     return t
#
#
# def _async_raise(tid, exctype):
#     import ctypes
#     import inspect
#     """raises the exception, performs cleanup if needed"""
#     tid = ctypes.c_long(tid)
#     if not inspect.isclass(exctype):
#         exctype = type(exctype)
#     res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
#     if res == 0:
#         raise ValueError("invalid thread id")
#     elif res != 1:
#         # """if it returns a number greater than one, you're in trouble,
#         # and you should call it again with exc=NULL to revert the effect"""
#         ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
#         raise SystemError("PyThreadState_SetAsyncExc failed")
#
#
# # 线程_停止
# def thread_stop(thread):
#     _async_raise(thread.ident, SystemExit)
#
#
# # 窗口_置顶
# def 窗口_置顶(hwnd):
#     import win32gui
#     """可行方案 demo"""
#     # 1.最小化  #2.被遮挡  #2种情况下 能置顶显示
#
#     # 如果是最小化:https://blog.csdn.net/qq_16234613/article/details/79155632
#     if win32gui.IsIconic(hwnd):
#         # print("检测,最小化")
#         # win32gui.ShowWindow(hwnd, win32con.SW_SHOWNOACTIVATE)  # 4 最小化用这个恢复 可以 #被遮挡不行
#         win32gui.ShowWindow(hwnd, 4)  # 4 最小化用这个恢复 可以 #被遮挡不行
#     else:
#         # print("检测,not最小化")
#         # win32gui.ShowWindow(hwnd, win32con.SW_SHOW)  # 8 被遮挡 用这个恢复 可以 #最小化不行
#         win32gui.ShowWindow(hwnd, 8)  # 8 被遮挡 用这个恢复 可以 #最小化不行
#
#     from win32com.client import Dispatch
#     Dispatch("WScript.Shell").SendKeys('%')  # 为了解决win32gui.SetForegroundWindow(hwnd)的bug
#     win32gui.SetForegroundWindow(hwnd)  # 置前显示
#
#
# # 枚举窗口hwnd_list的代码:
# def 窗口_枚举():
#     import win32gui
#     # 返回 hwndList
#     hWndList = []
#     win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
#     # print(hWndList)
#     return hWndList
#
#
# # 窗口_查找窗口_支持模糊类名和标题
# def 窗口_FindWindow_模糊(classname="", title=""):
#     import win32gui
#     hWndList = []
#     win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
#     # print(hWndList)
#     for hwnd in hWndList:
#         t = win32gui.GetWindowText(hwnd)
#         c = win32gui.GetClassName(hwnd)
#         # print(t, c)
#         if (title in t) and (classname in c):
#             # print(t, c)
#             # print("t, title", t, title)
#             return hwnd
#     return None
#
#
# # 窗口_查找窗口
# def 窗口_FindWindow(classname, title):
#     import win32gui
#     # hwnd = win32gui.FindWindow("Chrome_WidgetWin_1", "Appium")
#     # hwnd = win32gui.FindWindow(classname, title)
#     return win32gui.FindWindow(classname, title)
#
#
# def 窗口_取子窗口句柄(父hwnd, 子窗口类名):
#     import win32gui
#     # win32gui.FindWindowEx()
#     # https://blog.csdn.net/seele52/article/details/17504925
#     # https://segmentfault.com/q/1010000004506806
#     # hWnd = win32.user32.FindWindowW('Notepad', None)
#     # hEdit = win32.user32.FindWindowExW(hWnd, None, 'Edit', None)
#
#     # 获取父句柄hwnd类名为clsname的子句柄
#     # hwnd1 = win32gui.FindWindowEx(hwnd, None, clsname, None)
#
#     return win32gui.FindWindowEx(父hwnd, None, 子窗口类名, None)
#
#
# # 获得当前鼠标位置
# def 窗口_取鼠标位置():
#     # def get_curpos():
#     # (37, 607)  元组方式
#     import win32gui
#     return win32gui.GetCursorPos()
#
#
# # 获得指定位置窗口句柄：
# def 窗口_取句柄_指定位置(pos):
#     # def get_win_handle(pos):
#     import win32gui
#     return win32gui.WindowFromPoint(pos)
#
#
# def 窗口_取句柄_GetMousePointWindow():
#     # def 窗口_取句柄_鼠标指向位置():
#     import win32gui
#     return win32gui.WindowFromPoint(win32gui.GetCursorPos())
#
#
# def 窗口_关闭(hwnd):
#     import win32gui
#     import win32con
#     # win32gui.PostMessage(win32lib.findWindow(classname, titlename), win32con.WM_CLOSE, 0, 0)
#     # win32gui.PostMessage(win32gui.findWindow(classname, titlename), win32con.WM_CLOSE, 0, 0)
#     win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
#
#
# def 窗口_取屏幕句柄():
#     import win32gui
#     return win32gui.GetDesktopWindow()
#
#
# def 窗口_取标题(hwnd):
#     import win32gui
#     return win32gui.GetWindowText(hwnd)
#
#
# def 窗口_取类名(hwnd):
#     import win32gui
#     return win32gui.GetClassName(hwnd)
#
#
# def 窗口_是否最小化(hwnd):
#     # 非最小化:0被遮挡,前台  最小化1
#     import win32gui
#     return win32gui.IsIconic(hwnd)
#
#
# def 窗口_GetClientRect(hwnd):
#     # (0, 0, 371, 863)         0,0,宽度,高度
#     import win32gui
#     return win32gui.GetClientRect(hwnd)
#
#
# def 窗口_GetWindowRect(hwnd):
#     # #(335, 0, 706, 863)    x1,y1,x2,y2  窗口坐标系
#     import win32gui
#     return win32gui.GetWindowRect(hwnd)
#     # def 窗口_GetWindowRect(hwnd):
#     #     import win32gui
#     #     rect = win32gui.GetWindowRect(hwnd)
#     #     return rect[0], rect[1]
#
#
# def 窗口_句柄_取进程ID(hwnd):
#     import win32process  # 进程模块
#     hid, pid = win32process.GetWindowThreadProcessId(hwnd)
#     # hid是线程id吗??
#     return pid
#
#
# def 鼠标_moveto(*args):  # 优势:支持 鼠标_moveto(x, y) 也支持鼠标_moveto((x,y))格式
#     # def 鼠标_moveto(x, y):
#     import win32api
#     # win32api.SetCursorPos([x, y])  #函数原型
#     # print(*args)
#     # print(args)
#     # print(len(args)) #这个没问题  2个参数就是args=(1, 2) len就是2 1个元组就是1
#     # print(len(*args))  #报错 会因为参数问题  *args是解包 解包后的2个int 是不能被len的
#     """
#     笔记:关于传入参数是否解包的问题:
#     比如传入2个参数x,y    def *args 实际用的时候 args就是原样x,y传入
#     比如传入1个参数(x,y)  def *args 实际用的时候 *args就是解包 (x,y)解包为x,y
#     另外:len(args) 就是args里面参数的个数,x,y就2个,(x,y)就1个
#     """
#     if len(args) == 1:
#         # win32api.SetCursorPos(list(*args))  ##这种可以鼠标_moveto((1,2))
#         win32api.SetCursorPos(*args)  # 这种可以鼠标_moveto((1,2))
#     if len(args) == 2:
#         win32api.SetCursorPos(args)  # 这种可以 鼠标_moveto(1,2)
#
#
# # print(*args[0],*args[1]) #错误 TypeError: print() argument after * must be an iterable, not int
# # win32api.SetCursorPos([*args]) #不解包的话,有一个会报错
# # win32api.SetCursorPos([args])
# # x,y=args
# # lis=list(*args)     #这种可以鼠标_moveto((1,2))  #这种不行 鼠标_moveto(1,2)
# # win32api.SetCursorPos(lis)
# # win32api.SetCursorPos([x, y])
#
# def 鼠标_LeftClick_X_Y(*args):
#     # 鼠标_点击坐标(102,637)
#     # 鼠标_点击坐标((102,637))
#     import win32api
#     import win32con
#     # if isinstance(args,tuple):
#     #     x, y = *args[0], *args[1]
#     if len(args) == 1:
#         x, y = *args[0], *args[1]
#         # win32api.SetCursorPos(*args)  #这种可以鼠标_moveto((1,2))
#     if len(args) == 2:
#         x, y = args
#         # win32api.SetCursorPos(args)  #这种可以 鼠标_moveto(1,2)
#     win32api.SetCursorPos((x, y))
#     win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
#     win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
#     '''原型
#     def click1(x,y):                #第一种  #前台
#         win32api.SetCursorPos((x,y))
#         win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
#         win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
#     #原文链接：https://blog.csdn.net/qq_16234613/article/details/79155632
#     '''
#
#
# def _鼠标_LeftDown():
#     # 左键 按下
#     import win32api
#     import win32con
#     win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)  # ; // 点下左键
#
#
# def _鼠标_LeftUp():
#     # 左键 弹起
#     import win32api
#     import win32con
#     win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)  # ; // 点下左键
#
#
# def _鼠标_RightDown():
#     # 右键 按下
#     import win32api
#     import win32con
#     win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)  # ; // 点下左键
#
#
# def _鼠标_RightUp():
#     # 右键 弹起
#     import win32api
#     import win32con
#     win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
#
#
# # 支持 左键/右键 + 单击/按下/放开
# def 鼠标_按键(键=0, 按键类型=0):
#     """
#     # 支持 左键/右键 + 单击/按下/放开
#     # 键 左键0 右键1
#     # 按键类型 默认为0 单击；1 #按下 2 #放开
#     """
#     import win32api
#     import win32con
#
#     if 键 == 0:
#         if 按键类型 == 0:
#             win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)  #
#             win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)  #
#         elif 按键类型 == 1:
#             win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)  #
#         elif 按键类型 == 2:
#             win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)  #
#     if 键 == 1:
#         if 按键类型 == 0:
#             win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)  #
#             win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
#         elif 按键类型 == 1:
#             win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)  #
#         elif 按键类型 == 2:
#             win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
#
#
# # 默认为0 单击；1 #按下 2 #放开
# def 键盘_按键(键代码, 按键类型=0):
#     # 默认为0 单击；1 #按下   2 #放开
#     # 键代码 可以去win32con里面的VK_部分找  也可以在网上直接找虚拟键码表
#     import win32api
#     import win32con
#
#     # if type(键代码) == type(1): pass
#     if isinstance(键代码, int): pass
#     # if type(键代码) == type("1"):
#     if isinstance(键代码, str):
#         # tod1 需要转换为键代码
#         # tod2 小写字母要转换为大写字母 再ord取键代码 只支持小写字符
#         键代码 = 键代码.upper()
#         键代码 = ord(键代码)
#
#     if 按键类型 == 0:
#         win32api.keybd_event(键代码, 0, 0, 0)  # Delete
#         win32api.keybd_event(键代码, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
#     elif 按键类型 == 1:
#         win32api.keybd_event(键代码, 0, 0, 0)
#     elif 按键类型 == 2:
#         win32api.keybd_event(键代码, 0, win32con.KEYEVENTF_KEYUP, 0)
#
#
# def 键盘_组合按键(*args):
#     """
#     *args 需要为键码数字  文本方式目前只支持"大写/小写"单个字母
#     示例1:键盘_组合按键(win32con.VK_LCONTROL, win32con.VK_MENU,"s")
#     示例1:键盘_组合按键(17,18,83)  #这里83是大写S的键码 小写的不能用与其它功能键重复
#     # 支持键码数字或者wincon常量
#     # 兼容大小写字母 比如ctrl+alt+s 和 ctrl+alt+S一致
#     """
#     import win32api
#     import win32con
#
#     # todo  没写完  #准备把
#     dic = {"ctrl": win32con.VK_LCONTROL,
#            "alt": win32con.VK_MENU,
#            "shift": win32con.VK_SHIFT,
#            "win": win32con.VK_LWIN
#            }
#
#     lis = list(args)
#     print(lis)
#     # ★对字母的处理 小写字母要转换成大写字母对应的键码
#     for i in range(len(lis)):
#         # print(lis[i])
#
#         # done 关于数字的处理
#         # if type(lis[i]) == type("文本"):
#         if type(lis[i]) is type("文本"):
#             lis[i] = lis[i].upper()  # 变大写
#             lis[i] = ord(lis[i])  # 取得键码数字
#             # print(lis[i])
#         # todo 这里要处理 文本长度是否异常
#         # todo 这里要处理是否都是键码
#         if type(lis[i]) is not int:
#             print("检测到非数字键码,异常")
#             return
#     for i in lis:
#         win32api.keybd_event(i, 0, 0, 0)  # 按下键码
#         print()
#         # todo 这里可以检测按键状态,调试输出
#     for i in lis:
#         win32api.keybd_event(i, 0, win32con.KEYEVENTF_KEYUP, 0)  # 弹起键码
#         # todo 这里可以检测按键状态,调试输出
#
#
# def 鼠标_消息(): pass
#
#
# def 键盘_消息(hwnd, 键代码, 状态=0, 是否功能键=False):
#     # 作用:发送 后台按键
#     # 状态  0=输入字符(大写) 1=输入字符(小写)  2=按下，3=放开，4=单击
#     # 是否功能键  默认为假：普通键   真:功能键 (为功能键可用于热键技能不输入字符)
#     import win32gui
#     if 是否功能键 is True:
#         # WM_SYSKEYDOWN = 260
#         # WM_SYSKEYUP = 261
#         按下 = 260
#         放开 = 261
#     else:
#         # WM_KEYDOWN = 256
#         # WM_KEYUP = 257
#         按下 = 256
#         放开 = 257
#     if 状态 == 0:
#         # WM_CHAR = 258
#         win32gui.PostMessage(hwnd, 258, 键代码, 0)
#     if 状态 == 1:
#         win32gui.PostMessage(hwnd, 按下, 键代码, 0)
#     if 状态 == 2:
#         win32gui.PostMessage(hwnd, 按下, 键代码, 0)
#     if 状态 == 3:
#         win32gui.PostMessage(hwnd, 放开, 键代码, 0)
#     if 状态 == 4:
#         win32gui.PostMessage(hwnd, 按下, 键代码, 0)
#
#
# def adb_tap(x, y, delay=0.5):
#     # 用来 运行 点击屏幕坐标命令  driver.tap()点击无效
#     import os
#     import time
#     # dx, dy = 544, 1346
#     # os.popen("adb shell input tap " + str(x) + " " + str(y))
#     cmd = "adb shell input tap {x} {y}".format(x=x, y=y)  # 不用转换为str 默认就转换了好像
#     # os.popen("adb shell input tap " + str(x) + " " + str(y))
#     os.popen(cmd)
#     time.sleep(delay)


# print("时间_取现行时间戳", 时间_取现行时间戳)

"""测试耗时:"""
# import time

# print(time.ctime(), '代码起始时间')

# print(res)

# print(time.ctime(), '代码结束时间')

"""测试耗时:"""
# import time

# t = time.time()

# print('代码开始,计时' , t )

# print(do something....)

# print( '代码结束.耗时:' , time.time()-t)


if __name__ == '__main__':
    import doctest

    # doctest.testmod(verbose=True)
    doctest.testmod()
