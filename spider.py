#coding=utf-8
"""
网页源链接

"""

import requests
import re
import time
import random
import chardet

from bs4 import BeautifulSoup

cookies = dict(_gscbrs_39188577='1', _gscu_39188577='99518459t609p540')

headers = {  # 请求头请求刷新验证码和发送post时需要使用
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://www.nm.zsks.cn/zy_3_1_2017/kl_11.html',
    'Connection': 'keep-alive'
}
url='http://www.nm.zsks.cn/zy_3_1_2017/kl_11.html'
r = requests.get(url, cookies=cookies)

print r.encoding
r.encoding = 'gbk'
print r.text

soup = BeautifulSoup(r.text, "html5lib", from_encoding='gbk')

with open('data/main.txt', 'w') as f:
    print >>f, r.text.encode('utf-8')
print soup.originalEncoding
print soup.prettify()

def login(username,password):
    headers = {     #请求头请求刷新验证码和发送post时需要使用
        'Host': '210.41.224.117',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://210.41.224.117/Login/xLogin/Login.asp',
        'Connection': 'keep-alive'
    }
    #99518459t609p540
    session = requests.Session()
    step1 = session.get("http://jxgl.cuit.edu.cn/Jxgl/Xs/MainMenu.asp")
    get_osid_url = re.compile(r'content="0;URL=(.*?)">') #获取含OSid的跳转网址
    osid_url = get_osid_url.findall(step1.text)
    step2 = session.get(osid_url[0])    #跳转，上文要点1
    get_codeKey = re.compile(r'var codeKey = \'(.*?)\';')   #在登陆页html中获取codeKey(参数k)
    codeKey = get_codeKey.findall(step2.text)
    timeKey = str(time.time())[:10] + str(random.randint(100, 999)) #生成参数t的值（时间戳+三位随机数）
    payload = {'k': codeKey[0], 't': timeKey}
    yzm_url='http://210.41.224.117/Login/xLogin/yzmDvCode.asp'
    yzmdata = session.get(yzm_url, params=payload, headers=headers)  #刷新验证码，上文要点2

    yzm = raw_input('please enter yzm: ')   #人工识别验证码后输入
    post_data = {
        'WinW': '1366',
        'WinH': '728',
        'txtId': username,
        'txtMM': password,
        'verifycode': yzm,
        'codeKey': codeKey[0],
        'Login': 'Check',
        'IbtnEnter.x': 10,
        'IbtnEnter.y': 10
    }
    post_url='http://210.41.224.117/Login/xLogin/Login.asp'
    step3 = session.post(post_url, data=post_data, headers=headers)   #post登陆数据
    return session
"""
cuitJWC=login('username','password')
con=cuitJWC.get('http://jxgl.cuit.edu.cn/JXGL/xs/MainMenu.asp')
con.encoding='gb2312'
print con.text
"""
