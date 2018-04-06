#coding=utf-8
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
from browser import headers,cookies
from db.major import Major



check_fileds = ['major_code', 'major_name' ,'num_of_admission',
        'lowest_apply_point','num_of_applicants', 'tuition_fee']




class MajorWebPage(object):

    def __init__(self):
        self.major = Major()
        self.fileds = ['code', 'name','plan_num', 'min_score', 'applicant_num_received'\
                       ,'tuition', 'location', 'notes', 'university_id']
        self.items = []
        self.type = type



    def parse(self, url='http://www.nm.zsks.cn/zy_3_1_2017/3_A_308_11.html'):

        r = requests.get(url, cookies=cookies)

        #print r.encoding
        r.encoding = 'gbk'
        self.items = []
        soup = BeautifulSoup(r.text, "html5lib", from_encoding='gbk')

        for row in soup.select('tr'):
            item = {}
            c = 0
            for d in row.children:
                if isinstance(d, bs4.element.Tag):
                    if d.name == 'td':
                        #print "%s," % d.string, self.fileds[c],
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

    def output_to_db(self, university_id, university_name):
        for idx, item in enumerate(self.items):
            #print item.get('min_score', '')
            if item.get('min_score', '') and item.get('min_score', '').isdigit():
                item['university_id'] = str(university_id)
                item['university_name'] = university_name
                self.major.insert_into_major(item)



if __name__ == '__main__':
    w = MajorWebPage()
    w.parse()
    w.output_to_db()

