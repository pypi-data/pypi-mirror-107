# 之所以不是JSON  而是JSON操作 是因为python自带json.py  import json.py会重复


def json_加载(s):
    import json
    #
    try:
        s = json.loads(s)
    except Exception:
        # print('直接进行json.loads(),捕捉到报错,重新进行json.dumps(),json.loads()进行加载')
        s = json.dumps(s)
        s = json.loads(s)
    # 返回json对象
    return s
