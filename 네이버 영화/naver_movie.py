#!/usr/bin/env python

'''
pip install requests
pip install beautifulsoup4

TODO LIST:

'''

################################################################################################################################################################
import csv

import requests
from bs4 import BeautifulSoup
################################################################################################################################################################



################################################################################################################################################################
# [함수] 상영중인 영화 목록 긁어와서 naver_movie.csv 파일로 저장 및 리스트 리턴
# GetNaverMovie(): List [[코드, 제목], ...]

def GetNaverMovie():
    # requests 보냄(네트워크 캡쳐된거 그대로 긁어와서 작성)
    response = requests.request(
        method = 'GET', #Request Method [GET, POST 등등]
        url = 'https://movie.naver.com/movie/running/current.nhn', #Request URL
        headers = { #Request Headers [보낼 헤더값 ]
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

    # BeautifulSoup에 response.text(requests 반환값)을 넣어줌
    bs = BeautifulSoup(response.text, 'html.parser')

    # 테스트
    # print(type(bs), '\n', bs) #타입: bs4.BeautifulSoup

    # HTML 소스를 보면 데이터들이 <ul class="lst_detail_t1"> 에 담겨져 있음을 확인 할 수 있다.
    # HTML 소스에서 <ul><li> 는 항목 리스트며
    # 이를 BeautifulSoup을 활용하여 ul 태그에 class값이 lst_detail_t1 이고 다음에 li값이 오니
    # ul.lst_detail_t1 > li 를 BeautifulSoup의 select를 사용하여 리스트들을 LstElement에 구해온다.
    #
    # TIP: css에서
    # class 는 . ex).클래스네임 / div.클래스네임
    # id 는 # ex)#아이디 / div.아이디
    # 이다.
    LstElement = bs.select('ul.lst_detail_t1 > li')

    # 테스트
    # print(type(LstElement)) #타입: List
    # print(type(LstElement[0])) #타입: bs4.BeautifulSoup.tag

    # 결과값 초기화
    Result = []

    # LstElement에 li 데이터들이 담겨있으므로, 하나하나 루프돌려 TmpEle1에 담아준다.
    for TmpEle1 in LstElement:
        # 딕셔너리 자료값 초기화
        TmpJSON1 = {} #{'title': '제목', 'code': '코드'}

        # ul > li 안에 제목은 <dl class="lst_dsc"> <dt class="tit"> <a> 의 InnerText에 담겨져있다.
        # 따라서 BeautifulSoup에서 구해온 ul > li 태그에서 목록에서
        # 추가적으로 select_one을 사용하여 a 태그 1개만 선택해주고 텍스트를 구해와 TmpJSON1에 넣어준다.
        #
        # 첨삭하면 'dl.lst_dsc > dt.tit > a' 요렇게도 가능하다.
        TmpJSON1['title'] = TmpEle1.select_one('dt.tit > a').get_text()

        # 마찬가지로 코드값은 <dl class="lst_dsc"> <dt class="tit"> <a> 의 href끝자리에 담겨져있다.
        # a 태그의 attribute를 구하는건
        # bs4.BeautifulSoup.tag['attribute 값']
        # 이렇게 사용하면된다.
        TmpStr1 = TmpEle1.select_one('dt.tit > a')['href']

        # a 태그의 href 값을 구해왔으니 끝에있는 코드값만 구해와준다.
        # /movie/bi/mi/basic.nhn?code=189069
        # string.find('검색어'): 해당 문자열이 있는 위치값
        # string[시작문자열위치:끝날문자열위치]: 시작문자열위치에서 끝날문자열위치까지의 문자열을 구해와준다.
        #
        # TmpStr1[TmpStr1.find('?code='):] 에서 +6을 안해주면 ?code=189069 이런식으로
        # 시작문자열 앞부분까지 긁어오니 +6 해주었다.
        TmpJSON1['code'] = TmpStr1[TmpStr1.find('?code=') +6:]

        # 결과값에 추가
        Result.append([TmpJSON1['code'], TmpJSON1['title']])
        
        # 테스트
        # print(TmpJSON1)
    
        #CSV 파일로 저장해준다.
        with open(r'.\naver_movie.csv', 'a', encoding='utf-8') as hFile:
            csvwriter = csv.DictWriter(hFile, fieldnames = ['title', 'code'])
            csvwriter.writerow(TmpJSON1)

    return Result


################################################################################################################################################################
# [함수] 상영중인 영화 최신 평점, 감상평 저장 및 리스트 리턴
# GetNaverMovieRate(영화 코드): List [[영화코드, 평점코드, 평점, 감상평], ...]

def GetNaverMovieRate(StrMovieCode):
    # StrMovieCode는 앞에서 말한 코드값
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
            # Referer 값에 code 파라미터는 url의 코드값에서 구해와진거
            'Referer': 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=' +StrMovieCode +'&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false',
            'Accept-Encoding': 'deflate',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5'
        }
    )

    bs = BeautifulSoup(response.text, 'html.parser')

    LstElement = bs.select('div.score_result > ul > li')

    Result = []
    for TmpEle1 in LstElement:
        # 초기화 값
        TmpJSON1 = {'movie_code': StrMovieCode}

        #
        #
        # 시간되면 이코드가 왜 작동하나 확인해보기..

        # TmpStr1 = TmpEle1.select_one('div.score_reple > dl > dd > a')['onclick']
        # TmpStr1 = TmpStr1[134:]
        # TmpJSON1['reple'] = TmpStr1[0:TmpStr1.find(' \', \'')]
        # TmpStr1 = TmpStr1[TmpStr1.find(' \', \'') +5:]
        # TmpJSON1['reple_code'] = TmpStr1[0:TmpStr1.find('\', \'point_after')]

        # TmpJSON1['reple_rate'] = TmpEle1.select_one('div.star_score > em').get_text()

        # Result.append([TmpJSON1['movie_code'], TmpJSON1['reple_code'], TmpJSON1['reple_rate'], TmpJSON1['reple']])
        #
        #


        #
        # 정석 코드
        #
        # 리플 구해오기
        # <div class="score_result"> 에 <ul>, <li> 의
        # <div class="score_reple">, <p>, <span id="_filtered_ment_0"> 값이 내용이므로
        # div.score_reple > p > span#_filtered_ment_0 가 되며,
        # id 값의 끝 _0은 증가하므로 span의 id값은 생략해줬다.
        TmpStr1 = TmpEle1.select_one('div.score_reple > p > span').get_text().strip()
        TmpJSON1['reple'] = TmpStr1

        # 리플의 id값 구해오기
        # <div class="score_reple">, <dl>, <dt>, <em>, <a> 의 onclick에 id값이 있으므로 긁어와준다.
        # ex)
        # javascript:showPointListByNid(17053236, 'after');parent.clickcr(this, 'ara.uid', '', '', event); return false;
        TmpStr1 = TmpEle1.select_one('div.score_reple > dl > dt > em > a')['onclick']

        # 30번째부터 콤마까지의 문자열이 리플의 id값이므로 잘라준다.
        TmpJSON1['reple_code'] = TmpStr1[30:TmpStr1.find(',')]

        # 리플의 평점 구해오기
        # <div class="star_score">의 <em>의 innerText가 평점이니 구해온다.
        TmpJSON1['reple_rate'] = TmpEle1.select_one('div.star_score > em').get_text()

        Result.append([TmpJSON1['movie_code'], TmpJSON1['reple_code'], TmpJSON1['reple_rate'], TmpJSON1['reple']])

        with open(r'.\naver_movie_review.csv', 'a', encoding='utf-8') as hFile:
            csvwriter = csv.DictWriter(hFile, fieldnames = ['movie_code', 'reple_code', 'reple_rate', 'reple'])
            csvwriter.writerow(TmpJSON1)

    return Result
    

################################################################################################################################################################
# 메인

# 테스트
#print(GetNaverMovie())
#print(GetNaverMovieRate('189069'))

TmpLst1 = GetNaverMovie()
for TmpLst2 in TmpLst1:
    GetNaverMovieRate(TmpLst2[0])