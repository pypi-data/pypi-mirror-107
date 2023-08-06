def 数组_到文本(数组, 连接符=''):  # python里面直接是 join
    # 原本是list 但是内置list()方法 会导致list()失效
    return 连接符.join(数组)



def list_去重复_找重复(lis):
    重复元素_list = []
    new_list = []
    for i in lis:
        if i not in new_list:
            new_list.append(i)
        else:
            # 重复元素_list.append(i)  # 写法1 这种写法 会导致 重复的元素 会重复添加进 如果不想这么重复 可以判断是否在 重复元素_list
            if i not in 重复元素_list: 重复元素_list.append(i)  # 写法2: 这种重复的元素 不会重复添加进来

    return new_list, 重复元素_list

def 数组_去重复_找重复(lis):
    重复元素_list = []
    new_list = []
    for i in lis:
        if i not in new_list:
            new_list.append(i)
        else:
            # 重复元素_list.append(i)  # 写法1 这种写法 会导致 重复的元素 会重复添加进 如果不想这么重复 可以判断是否在 重复元素_list
            if i not in 重复元素_list: 重复元素_list.append(i)  # 写法2: 这种重复的元素 不会重复添加进来

    return new_list, 重复元素_list


