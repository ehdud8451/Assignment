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
# [함수] 상영중인 영화 목록 긁어와서 naver_movie.csv 파일로 저장 및 리스트 리턴
# GetNaverMovie(): List [[코드, 제목], ...]
def GetNaverMovie():
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

    Result = []
    for TmpEle1 in LstElement:
        TmpJSON1 = {'title': '', 'code': ''}
        TmpJSON1['title'] = TmpEle1.select_one('dt.tit > a').get_text()
        TmpStr1 = TmpEle1.select_one('dt.tit > a')['href']
        TmpJSON1['code'] = TmpStr1[TmpStr1.find('?code=') +6:]
        Result.append([TmpJSON1['code'], TmpJSON1['title']])
    
        with open(r'.\naver_movie.csv', 'a', encoding='utf-8') as hFile:
            csvwriter = csv.DictWriter(hFile, fieldnames = ['title', 'code'])
            csvwriter.writerow(TmpJSON1)

    return Result

################################################################################################################################################################
# [함수] 상영중인 영화 최신 평점, 감상평 저장 및 리스트 리턴
# GetNaverMovieRate(영화 코드): List [[영화코드, 평점코드, 평점, 감상평], ...]
def GetNaverMovieRate(StrMovieCode):
    response = requests.request(
        method = 'GET',
        url = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=' +StrMovieCode +'&type=after&onlyActualPointYn=N&onlySpoilerPointYn=N&order=newest',
        headers = {
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'iframe',
            'Referer': 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=' +StrMovieCode +'&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false',
            'Accept-Encoding': 'deflate',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5'
        }
    )

    bs = BeautifulSoup(response.text, 'html.parser')

    LstElement = bs.select('div.score_result > ul > li')

    Result = []
    for TmpEle1 in LstElement:
        TmpJSON1 = {'movie_code': StrMovieCode, 'reple_code': '', 'reple_rate': '', 'reple': ''}

        TmpStr1 = TmpEle1.select_one('div.score_reple > dl > dd > a')['onclick']
        TmpStr1 = TmpStr1[134:]
        TmpJSON1['reple'] = TmpStr1[0:TmpStr1.find(' \', \'')]
        TmpStr1 = TmpStr1[TmpStr1.find(' \', \'') +5:]
        TmpJSON1['reple_code'] = TmpStr1[0:TmpStr1.find('\', \'point_after')]

        TmpJSON1['reple_rate'] = TmpEle1.select_one('div.star_score > em').get_text()

        Result.append([TmpJSON1['movie_code'], TmpJSON1['reple_code'], TmpJSON1['reple_rate'], TmpJSON1['reple']])

        with open(r'.\naver_movie_review.csv', 'a', encoding='utf-8') as hFile:
            csvwriter = csv.DictWriter(hFile, fieldnames = ['movie_code', 'reple_code', 'reple_rate', 'reple'])
            csvwriter.writerow(TmpJSON1)

    return Result
    

TmpLst1 = GetNaverMovie()
for TmpLst2 in TmpLst1:
    GetNaverMovieRate(TmpLst2[0])
