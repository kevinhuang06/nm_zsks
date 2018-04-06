#coding=utf-8
# 愿景的推动者
import os
import requests
import re
import time
import random
import chardet


import bs4
from bs4 import BeautifulSoup
import MySQLdb
from urlparse import urljoin
from collections import OrderedDict
from browser import headers,cookies
from db.toudang import TouDang

table = 'applicant'


class TouDangWebPage(object):

    def __init__(self):
        self.toudang = TouDang()
        self.fileds = ['toudang_score', 'score', 'ethnic', 'gender'\
            , 'major_1', 'major_2', 'major_3', 'major_4', 'major_5', 'major_6', 'obey_tiaoji','patch']
        self.items = []
        self.type = type


    def parse(self, url = 'http://www.nm.zsks.cn/zy_3_1_2017/3_B_304_11_detail.html'):

        r = requests.get(url, cookies=cookies)
        r.encoding = 'gbk'


        soup = BeautifulSoup(r.text, "html5lib", from_encoding='gbk')
        '''
            with open('data/main.txt', 'w') as f:
                print >>f, r.text.encode('utf-8')
            print soup.originalEncoding
            print soup.prettify()
        '''
        self.items =[]
        for row in soup.select('tr'):
            item={}
            c = 0
            for d in row.children:
                if isinstance(d, bs4.element.Tag):
                    if d.name == 'td':
                        item[self.fileds[c]] = d.text
                        c += 1
                        if d.string=='294':
                            pass
                        for o in d.children:
                            if o.name == 'a':
                                href = o.attrs.get('href')
                                if 'http' not in href:
                                    href = urljoin('http://www.nm.zsks.cn', href)
                                item[self.fileds[c]] = href
#                                print href, c, self.fileds[c]
                                c += 1
            self.items.append(item)

    def output_to_db(self, university_id, university_name):

        for idx, item in enumerate(self.items):
            if item.has_key('toudang_score') and item.get('toudang_score', '').isdigit():
                item['university_id'] = str(university_id)
                item['university_name'] = university_name
                self.toudang.insert_into_toudang(item)



