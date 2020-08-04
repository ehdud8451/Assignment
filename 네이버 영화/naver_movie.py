#!/usr/bin/env python

'''
pip install requests
pip install beautifulsoup4

TODO LIST:

'''

################################################################################################################################################################
import os
import csv

import requests
from bs4 import BeautifulSoup


# 전역 상수 및 변수

################################################################################################################################################################

################################################################################################################################################################
# Main

response = requests.request(
    method = 'GET',
    url = 'https://movie.naver.com/movie/running/current.nhn',
    headers = {
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Encoding': 'deflate',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5'
    }
)

bs = BeautifulSoup(response.text, 'html.parser')

LstElement = bs.select('ul.lst_detail_t1 > li')

for TmpEle1 in LstElement:
    TmpJSON1 = {'title': '', 'code': '0'}
    TmpJSON1['title'] = TmpEle1.select_one('dt.tit > a').get_text()
    TmpStr1 = TmpEle1.select_one('dt.tit > a')['href']
    TmpJSON1['code'] = TmpStr1[TmpStr1.find('?code=') +6:]
    
    with open(r'.\naver_movie.csv', 'a', encoding='utf-8') as hFile:
        fieldname = ['title', 'code']
        csvwriter = csv.DictWriter(hFile, fieldnames = fieldname)
        csvwriter.writerow(TmpJSON1)

print(len(LstElement),'개 추가 완료!')
