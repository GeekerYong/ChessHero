import requests
from bs4 import BeautifulSoup

# 百度结果分析部分参考：https://github.com/wuditken/MillionHeroes

# 定义返回的result类
class Result(object):

    def __init__(self, r_index,  r_abstract):  # id似乎占用了内部名称，那就用index来代替吧
        self.__index = r_index
        self.__abstract = r_abstract

    @property
    def index(self):
        return self.__index

    @property
    def abstract(self):
        return self.__abstract


def page(html):
    # 初始化
    soup = BeautifulSoup(html, 'lxml')
    results = []
    # 获取结果html
    result_set = soup.find(id='content_left')
    result_set = result_set.find_all('div', class_='c-container')
    for i in range(len(result_set)):  # 因为要index所以就用range来
        result = result_set[i]  # 其实就是result_div
        c_abstract = __get_abstract(result)  # 同title
        result = Result(i + 1, c_abstract)
        results.append(result)
    return results


# 获取abstract
def __get_abstract(result_div):
    if 'result-op' not in result_div['class']:
        r_from = result_div.find(class_='c-abstract')
        if not r_from:
            return None
        for em in r_from.find_all('em'):
            em.unwrap()
        return r_from.get_text()
    else:
        return '广告信息'


