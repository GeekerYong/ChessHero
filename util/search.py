# -*- coding:utf-8 -*- 
#  @Time : 2018-01-09 11:24
#  @Author : Khazix
#  @File : search.py
#  @Description:
#            
#   --Input:
#   --Output:
import urllib
from bs4 import BeautifulSoup
import re
import string
import sys
import util.process as pro

from threading import Thread


class GetUrlThread(Thread):
    def __init__(self, url, keyword, assword):
        self.url = url
        self.keyword = keyword
        self.assword = assword
        super(GetUrlThread, self).__init__()

    def run(self):
        resp = urllib.request.urlopen(self.url)
        content = resp.read().decode('utf-8')
        # 获取前几个搜索结果的摘要
        self.result = pro.page(content)
        soup = BeautifulSoup(content, "lxml")
        # 获取搜索到的结果数目
        site = str(soup.find(class_="nums").get_text())
        self.num = site.split('约')[1]
        # 统计词频
        self.counts = content.count(self.assword)

    def get_result(self):
        try:
            return self.result, self.num, self.counts
        except Exception:
            return None


def get_search_result(keyword, asswords=[]):
    score = []
    absts = []
    counts = []
    # 多线程版
    threads = []
    for asword in asswords:
        quewords = keyword + ' ' + asword
        t = GetUrlThread("http://www.baidu.com/s?wd=" + urllib.parse.quote(quewords), keyword, asword)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
        results, num, count = t.get_result()
        score.append(num)
        absts.append(results)
        counts.append(count)
    # print(score)
    return score, absts, counts

if __name__ == '__main__':
    get_search_result(u'湖南省 洪泽湖')
