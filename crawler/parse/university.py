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
from db.batch import Batch
from browser import headers,cookies
from major import MajorWebPage
from toudang import TouDangWebPage

head = {
    u'': ['empty'],
    u'批次': ['batch_info'],
    u'院校代号': ['code'],
    u'院校名称': ['name','major_detail_url'],
    u'计划数': ['plan_num',],
    u'预计1:1投档最低分': ['min_score_1vs1'],
    u'投档比例': ['toudang_proportion'],
    u'预计投档最低分': ['min_score'],
    u'应投档人数': ['applicant_num_needed'],
    u'已报人数': ['applicant_num_received','toudang_detail_url'],
    u'缺档人数': ['quedang_num'],
    u'招生章程': ['admission_guide_desc','admission_guide_url']
}

class UniveristyWebPage(object):

    def __init__(self, type):
        self.uni = University()
        self.b = Batch()
        self.fileds = []
        #['code','name','major_detail_url','plan_num',\
   #'min_score','toudang_proportion','min_score_1vs1','applicant_num_needed',\
   # 'applicant_num_received','toudang_detail_url','quedang_num','admission_guide_desc','admission_guide_url']
        self.items = []
        self.type = type
        self.major = MajorWebPage()
        self.toudang = TouDangWebPage()
        self.batch = u'zy_3_1_2017' #本科一批第一次网报
        self.create_dir()

    def download_all(self, url):
        r = requests.get(url, cookies=cookies, headers=headers,timeout=1)
        #print r.encoding
        r.encoding = 'gbk'
        # 存储
        with open(os.path.join(self.storage, os.path.basename(url)), 'w') as f:
            print >>f, r.text.encode('utf-8')
        # 解析html
        soup = BeautifulSoup(r.text, "html5lib", from_encoding='gbk')


        for row in soup.select('tr'):
            for d in row.children:
                if isinstance(d, bs4.element.Tag):
                    if d.name == 'td':
                        for o in d.children:
                            if o.name == 'a':
                                href = o.attrs.get('href')
                                if 'http' not in href:
                                    href = urljoin('http://www.nm.zsks.cn', href)
                                    # 下载详情页
                                    #print href

                                    s_path = os.path.join(self.storage, os.path.basename(href))
                                    if os.path.exists(s_path):
                                        continue
                                    r = None
                                    try:
                                        r = requests.get(href, cookies=cookies, headers=headers, timeout=1)
                                    except:
                                        if 'javascript:history' not in href:
                                            print 'fail download {}'.format(href)
                                        continue
                                    if r:
                                        print href
                                        r.encoding = 'gbk'
                                        with open(s_path, 'w') as f:
                                            print >> f, r.text.encode('utf-8')



    def parse(self, url):
        r = requests.get(url, cookies=cookies)
        #print r.encoding
        r.encoding = 'gbk'
        # 解析html
        soup = BeautifulSoup(r.text, "html5lib", from_encoding='gbk')


        self.items = []
        for row in soup.select('tr'):
            item = {'type': self.type}
            c = 0
            for d in row.children:
                if isinstance(d, bs4.element.Tag):
                    if d.name == 'td':
                        print "%s," % d.string, self.fileds[c]
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

    def parse_local(self, path, batch_id):
        # 解析html
        with open(path) as f:
            soup = BeautifulSoup(f.read(), "html5lib", from_encoding='utf-8')


        self.items = []
        head_ready = False
        for row in soup.select('tr'):
            item = {'batch_id': batch_id}
            c = 0
            if not head_ready and self.fileds:
                if u'code' in self.fileds:
                    # 表示已经提取完表头
                    if self.fileds[-1] == 'empty':
                        self.fileds = self.fileds[:-1]
                        self.fileds.extend(head[u'招生章程'])
                    head_ready = True
                else:
                    # 提取到假的表头
                    self.fileds = []
            for d in row.children:
                if isinstance(d, bs4.element.Tag):
                    if d.name == 'td':
                        if not head_ready and d.text in head:  # 表头行
                            self.fileds.extend(head[d.text])
                        if head_ready: # 表头初始化后,才能用
                            #print d.text,len(self.fileds),c,self.fileds[c]
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
            # 去除空的项目
            if 'empty' in item:
                item.pop('empty')
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

    def create_dir(self):

        prefix = '../../data/'
        self.storage = os.path.join(prefix, self.batch)
        if not os.path.exists(self.storage):
            os.makedirs(self.storage)


def crawl():
    a = {
        u'普通文科': 'http://www.nm.zsks.cn/zy_3_1_2017/3_A_11.html',
        u'普通理科': 'http://www.nm.zsks.cn/zy_3_1_2017/3_B_11.html',
        u'蒙授文科': 'http://www.nm.zsks.cn/zy_3_1_2017/3_C_11.html',
        u'蒙授理科': 'http://www.nm.zsks.cn/zy_3_1_2017/3_D_11.html',
    }
    for k in a:
        print k, a[k]
        wizard = UniveristyWebPage(k)
        wizard.download_all(a[k])

def parse():
    b = {
        u'普通文科': '../../data/zy_3_1_2017/3_A_11.html',
        u'普通理科': '../../data/zy_3_1_2017/3_B_11.html',
        u'蒙授文科': '../../data/zy_3_1_2017/3_C_11.html',
        u'蒙授理科': '../../data/zy_3_1_2017/3_D_11.html',
    }

    for k,p in b.items():
        wizard = UniveristyWebPage(p)
        batch_id = wizard.b.batch_id(p)
        print batch_id
        wizard.parse_local(p, batch_id)
        try:
            wizard.output_to_db()
        except:
            with open('exp','a') as f:
                print >>f, k,p

if __name__ == '__main__':
    # crawl()
    parse()






