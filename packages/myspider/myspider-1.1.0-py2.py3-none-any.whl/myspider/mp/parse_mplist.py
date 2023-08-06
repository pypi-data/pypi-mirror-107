# coding: utf-8

"""
微信公众号文章列表解析
"""

import html, re, json

class ParseMpList():
    """
    微信公众号文章列表解析
    数据来源：中间人劫持windwos微信客户端公众号文章列表
    有两种方式，1. 第一页是html页面，2. 第一页之后都是json格式的数据
    解析目标：
    1. 标题
    2. 链接
    3. 发布日期
    4. 封面
    5. 公众号名称描述和id
    """
    def __init__(self) -> None:
        print("create ParseMplist Success")

    def parse_html(self, text):
        result = {}
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line[:4] != "var ":
                continue
            nickname = self.match_nickname(line)
            if nickname:
                result["nickname"] = nickname
            biz = self.match_biz(line)
            if biz:
                result["biz"] = biz
            msg_list = self.match_msg_list(line)
            if msg_list:
                result["msg_list"] = msg_list
        result = self.format_result(result)
        # print(json.dumps(result))
        print("done")
        return result

    def match_nickname(self, line):
        # var nickname = "新华社".html(false) || "";
        tag = "var nickname = "
        if line[:len(tag)] != tag:
            return
        r = re.findall(tag + "\"([^\"]{1,})\"", line)
        if r:
            return r[0]

    def match_biz(self, line):
        # var __biz = "MzA4NDI3NjcyNA==";
        tag = "var __biz = "
        if line[:len(tag)] != tag:
            return
        r = re.findall(tag + "\"([^\"]{1,})\"", line)
        if r:
            return r[0]

    def match_msg_list(self, line):
        # var msgList = '{&quot;list&quot;:[{&quot}'
        tag = "var msgList = "
        if line[:len(tag)] != tag:
            return
        line = line[len(tag):]
        line = line.strip(";")
        line = line.strip("'")
        line = line.strip("\"")
        line = html.unescape(line)
        line = json.loads(line)
        return line

    def get_list(self, v):
        """
        解析json，返回重要的字段
        包括
        id title, datetime, url, cover
        """
        try:
            comm_msg_info = v["comm_msg_info"]
            app_msg_ext_info = v["app_msg_ext_info"]
            tid = comm_msg_info["id"]
            ctime = comm_msg_info["datetime"]
            title = app_msg_ext_info["title"]
            content_url = app_msg_ext_info["content_url"]
            cover = app_msg_ext_info.get("cover")
        except Exception as e:
            print(e)
            return

        item = {
            "id": tid,
            "datetime": ctime,
            "title": title,
            "url": content_url,
            "cover": cover,
        }
        return item

    def format_result(self, result):
        mp_list = []
        for v in result["msg_list"]["list"]:
            item = self.get_list(v)
            if not item:
                continue
            mp_list.append(item)
        result["msg_list"] = mp_list
        return result

    def parse_json(self, text: str):
        """
        从第二页开始的json返回数据
        """
        jtext = json.loads(text)
        if jtext.get("ret") != 0:
            print("error input")
            return
        general_msg_list = jtext.get("general_msg_list")
        if not general_msg_list:
            return
        r = json.loads(general_msg_list)
        msg_list = []
        for v in r["list"]:
            item = self.get_list(v)
            if not item:
                continue
            msg_list.append(item)
        if not msg_list:
            return
        url = msg_list[0]["url"]
        params = self.get_url_params(url)
        result = {
            "msg_list": msg_list,
            "can_msg_continue": jtext.get("can_msg_continue"),
            "msg_count": jtext.get("msg_count"),
            "next_offset": jtext.get("next_offset"),
            "biz": params.get("__biz"),
        }
        return result

    def get_url_params(self, url):
        """
        从微信url链接中提取参数
        "http://mp.weixin.qq.com/s?
        __biz=MzA4NDI3NjcyNA==
        &mid=2649658395
        &idx=1
        &sn=e9a452afd05ac0eaccd0c04aabbff322
        &chksm=87f39080b0841996cfe9afb3f836ade9b2dcd99f09fe1166b2dba653d7c832205cf1e571b1c5
        &scene=27#wechat_redirect",
        """
        result = {}
        url = url.split("#")[0]
        param = url.split("?")[-1]
        kvalues = param.split("&")
        for kvalue in kvalues:
            kvs = kvalue.split("=")
            if len(kvs) < 2:
                continue
            result[kvs[0]] = kvs[1]
        return result


