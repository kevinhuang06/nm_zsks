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
        self.batch = u'zy_61_71_2017'  # 本科二批B第一次网报
        self.create_dir()

    def download_all(self, url):
        r = requests.get(url, cookies=cookies, headers=headers, timeout=2)
        # print r.encoding
        r.encoding = 'gbk'
        # 存储
        with open(os.path.join(self.storage, os.path.basename(url)), 'w') as f:
            print >> f, r.text.encode('utf-8')
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
                                    # print href

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

    def create_dir(self):

        prefix = '../../data/'
        self.storage = os.path.join(prefix, self.batch)
        if not os.path.exists(self.storage):
            os.makedirs(self.storage)

if __name__ == '__main__':
    a = {
        '普通文科': 'http://www.nm.zsks.cn/zy_61_71_2017/A_11.html',
        '普通理科': 'http://www.nm.zsks.cn/zy_61_71_2017/B_11.html',
        '蒙授文科': 'http://www.nm.zsks.cn/zy_61_71_2017/C_11.html',
        '蒙授理科': 'http://www.nm.zsks.cn/zy_61_71_2017/D_11.html',
        '汉授美术': 'http://www.nm.zsks.cn/zy_61_71_2017/E_11.html',
        '蒙授美术': 'http://www.nm.zsks.cn/zy_61_71_2017/F_11.html',
        '汉授音乐': 'http://www.nm.zsks.cn/zy_61_71_2017/G_11.html',
        '蒙授音乐': 'http://www.nm.zsks.cn/zy_61_71_2017/H_11.html',
        '其他艺术': 'http://www.nm.zsks.cn/zy_61_71_2017/I_11.html',
        '蒙授其他艺术': 'http://www.nm.zsks.cn/zy_61_71_2017/J_11.html',
        '汉授编导': 'http://www.nm.zsks.cn/zy_61_71_2017/@_11.html',
        '汉授体育': 'http://www.nm.zsks.cn/zy_61_71_2017/K_11.html',
        '蒙授体育': 'http://www.nm.zsks.cn/zy_61_71_2017/L_11.html',
        '计算机类': 'http://www.nm.zsks.cn/zy_61_71_2017/M_11.html',
        '农学类': 'http://www.nm.zsks.cn/zy_61_71_2017/N_11.html',
        '牧医类': 'http://www.nm.zsks.cn/zy_61_71_2017/O_11.html',
        '烹饪类': 'http://www.nm.zsks.cn/zy_61_71_2017/P_11.html',
        '财会类': 'http://www.nm.zsks.cn/zy_61_71_2017/Q_11.html',
        '美工设计类': 'http://www.nm.zsks.cn/zy_61_71_2017/R_11.html',
        '旅游类': 'http://www.nm.zsks.cn/zy_61_71_2017/S_11.html',
        '汽驾类': 'http://www.nm.zsks.cn/zy_61_71_2017/T_11.html',
        '建筑类': 'http://www.nm.zsks.cn/zy_61_71_2017/U_11.html',
        '机电类': 'http://www.nm.zsks.cn/zy_61_71_2017/V_11.html',
        '蒙牧医类': 'http://www.nm.zsks.cn/zy_61_71_2017/W_11.html',
        '化工类': 'http://www.nm.zsks.cn/zy_61_71_2017/X_11.html',
        '幼师类': 'http://www.nm.zsks.cn/zy_61_71_2017/Y_11.html',
        '医学类': 'http://www.nm.zsks.cn/zy_61_71_2017/Z_11.html',
        '体育类': 'http://www.nm.zsks.cn/zy_61_71_2017/0_11.html',
        '采矿类': 'http://www.nm.zsks.cn/zy_61_71_2017/1_11.html'
    }
    for k in a:
        print k, a[k]
        wizard = UniveristyWebPage(k)
        wizard.download_all(a[k])
        #wizard.download_majors()
        # 下载学校页
        #wizard.parse(a[k])
        #wizard.output_to_db()
        # 下载专业详情页
        #wizard.download_majors()
        # 下载投档记录页
        #wizard.download_toudang_record()
