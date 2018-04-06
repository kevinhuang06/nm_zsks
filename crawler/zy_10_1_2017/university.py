#coding=utf-8
"""
网页源链接

"""

import os
import requests
import re
import time
import random
import chardet


import bs4
from bs4 import BeautifulSoup

from urlparse import urljoin
from db.university import University
from browser import headers,cookies
from major import MajorWebPage
from toudang import TouDangWebPage

class UniveristyWebPage(object):

    def __init__(self, type):
        self.uni = University()
        self.fileds = ['code','name','major_detail_url','plan_num',\
    'min_score_1vs1','applicant_num_needed',\
    'applicant_num_received','toudang_detail_url','quedang_num','admission_guide_desc','admission_guide_url']
        self.items = []
        self.type = type
        self.major = MajorWebPage()
        self.toudang = TouDangWebPage()

    def parse(self, url):
        r = requests.get(url, cookies=cookies)
        #print r.encoding
        r.encoding = 'gbk'
        # 解析html
        soup = BeautifulSoup(r.text, "html5lib", from_encoding='gbk')
        '''
        with open('data/main.txt', 'w') as f:
            print >> f, r.text.encode('utf-8')
        print soup.originalEncoding
        # print soup.prettify()
        '''
        self.items = []
        for row in soup.select('tr'):
            item = {'type': self.type}
            c = 0
            for d in row.children:
                if isinstance(d, bs4.element.Tag):
                    if d.name == 'td':
                        #print "%s," % d.string, self.fileds[c]
                        item[self.fileds[c]] = d.text
                        c += 1
                        if d.text == '294':
                            pass
                        for o in d.children:
                            if o.name == 'a':
                                href = o.attrs.get('href')
                                if 'http' not in href:
                                    href = urljoin('http://www.nm.zsks.cn', href)
                                item[self.fileds[c]] = href
                                #print href, c, self.fileds[c]
                                c += 1
            self.items.append(item)

    def output_to_db(self):
        for idx, item in enumerate(self.items):
            if item.has_key('admission_guide_url') and 'http' in item['admission_guide_url']:
                self.uni.insert_into_university(item)

    def download_majors(self):
        s = time.time()
        for id, name, url in self.uni.get_major_details():
            self.major.parse(url)
            self.major.output_to_db(id, name)
            print '-'*25
        print time.time() - s

    def download_toudang_record(self):
        s = time.time()
        for id, name, url in self.uni.get_toudang_details():
            self.toudang.parse(url)
            self.toudang.output_to_db(id, name)
            print '-' * 25
        print time.time() - s

if __name__ == '__main__':
    a = {
        u'本科一批B普通文科': 'http://www.nm.zsks.cn/zy_C_1_2017/C_A_3.html',
        u'本科一批B普通理科': 'http://www.nm.zsks.cn/zy_C_1_2017/C_B_3.html'
    }
    for k in a:
        print k, a[k]
        wizard = UniveristyWebPage(k)
        # 下载学校页
        wizard.parse(a[k])
        wizard.output_to_db()
        # 下载专业详情页
        wizard.download_majors()
        # 下载投档记录页
        wizard.download_toudang_record()
