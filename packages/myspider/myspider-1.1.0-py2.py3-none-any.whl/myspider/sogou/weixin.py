# coding: utf-8

"""
搜狗微信搜索
"""

import logging
import requests, json, time
from myspider.utils import request
from bs4 import BeautifulSoup

mlog = logging.getLogger("mlog")


class ExceptWeixin(Exception):
    pass

class ExceptEnd(Exception):
    pass

class SearchWeixin():
    def __init__(self, url, params=None, **kwargs) -> None:
        self.url = url
        self.params = params
        self.kwargs = kwargs
        self.data = None
        self.init()

    def init(self):
        """
        检测参数是否符合要求
        """
        pass

    @property
    def _headers(self):
        h = {
            "User-Agent": request.random_ua()
        }
        return h
    
    def _do_get(self, url, params=None, **kwargs):
        data = None
        maxsize = 1024*1024*10
        s_time = time.time()
        with requests.get(url, headers=self._headers, timeout=35, stream=True) as r:
            if r.status_code != 200:
                raise ExceptEnd("get url[{}] error, status_code[{}]".format(url, r.status_code))
            for chunk in r.iter_content(chunk_size=1024*20):
                if not data:
                    data = chunk
                    continue
                data += chunk
                if len(data) >= maxsize:
                    raise ExceptEnd("data too big[{}], maxsize[{}MB]".format(url, round(maxsize/1024/1024, 2)))
        decode = False
        for encode in ["utf-8", "gb2312"]:
            try:
                data = data.decode(encode)
                decode = True
                break
            except:
                pass
        if not decode:
            raise ExceptEnd("decode data error")
        mlog.info("success time[{}s], size[{}MB], url[{}]".format(round(time.time()-s_time, 2), round(len(data)/1024/1024, 2), url))
        return data

    def _get(self, url, params=None, **kwargs):
        for _ in range(3):
            try:
                data = self._do_get(url, params, **kwargs)
                return data
            except ExceptEnd as e:
                raise e
            except Exception as e:
                mlog.error(e)
                continue

    def result(self):
        data = self._get(self.url, self.params, **self.kwargs)
        if not data:
            return
        self.data = data
        self.decode_data()

    def decode_data(self) -> list:
        """
        解析网络数据
        解析Sogou 微信 搜索结果页面
        """
        result_list = []
        soup = BeautifulSoup(self.data,'html.parser')
        for v in soup.select("div.txt-box"):
            try:
                link = v.select("h3 a")
                t_info = v.select("div.s-p")
                if not t_info:
                    # mlog.error("没有解析到时间")
                    continue
                if not link:
                    # mlog.error("没有解析到链接")
                    continue
                title = link[0].text
                tdetail = t_info[0]["t"]
                url = link[0]["href"]
                if "http" not in url:
                    url = "https://weixin.sogou.com" + url
                item = {"title": title, "url": url, "time": tdetail}
                result_list.append(item)
            except Exception as e:
                # mlog.debug("解析Sogou标题和链接异常[{}]".format(e))
                continue
        return result_list