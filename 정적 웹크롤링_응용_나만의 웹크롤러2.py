'''
앞서 진행한 내용은, 네이버 뉴스 목록에 뜨는 기사들의 제목과 url, 신문사 정보만 추출하는 것에 그침.

이번목표는 각 기사들의 url을 타고 들어가 기사 내용 전문을 크롤링 하는 것.

but 문제점: "네이버뉴스" 기사의 경우 여러 신문사의 기사를 모아놓음 (동아일보, 조선일보...등)
신문사 마다 html구조가 모두 다르기 때문에 각각의 크롤러를 만들어줘야함... 

 -> 해결방법

 '네이버 뉴스 홈' 이라는 플랫폼 안에서 동일한 html구조를 가진 기사들을 크롤링 하는 것'
 즉, 동일한 html 구조를 가진 뉴스 플랫폼(=동일한 html구조로 뉴스를 모아놓는 곳)에서 신문기사를 크롤링 하자!

''' 

<프로그램 돌아가는 방식>
앞선 방식과 마찬가지로 main함수/crawler함수를 거침
-> get_news함수를 통해 뉴스 본문 전체를 크롤링
-> excel_make함수를 통해 엑셀로 최종저장



# 라이브러리 import

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
RESULT_PATH = 'C:/git_project/python web crolling/'
now = datetime.now()


# crawler 함수

def crawler(maxpage,query):
    
    page = 1
    f = open('C:/git_project/python web crolling/contents_text.txt','w',encoding = 'utf-8')
            
    while page <= int(maxpage):

        maxpage_t = (int(page)-1)*10+1
        
        url = "https://search.naver.com/search.naver?&where=news&query=" + query + " &start=" + str(maxpage_t)
    
        response = requests.get(url)
        
        html = response.text  

        soup = BeautifulSoup(html, 'html.parser') # url 파싱
        
        atags = soup.select('._sp_each_url')

        # 기능 추가 - 네이버 뉴스 홈에 등록된 기사인지 확인하고, 맞으면 해당 url을 get_news로 보냄       

        for atag in atags:
            try: 
                if atag["href"].startswith("https://news.naver.com"):
                    
                    news_detail = get_news(atag["href"])

                    # get_news를 통해 얻은 내용을 txt파일에 저장
                    f.write("{}\t{}\t{}\t{}\t{}\n".format(news_detail[1], news_detail[4], news_detail[0], news_detail[2],news_detail[3]))
                    
            except Exception as e:
                print(e)
                continue
            
        page += 1


# get_news 함수 - 네이버 뉴스홈에 등록된 기사의 본문을 크롤링


def get_news(n_url):
    news_detail = [] # 내용을 담을 빈 리스트 만들기

    req = requests.get(n_url)
    soup = BeautifulSoup(req.content, 'html.parser') # url 파싱
    
    title = soup.select('h3#articleTitle')[0].text # select문을 통해서 리스트를 추출해옴. 리스트는 text기능이 없으므로 [0]을 통해 인덱싱 해주어야함
    news_detail.append(title)  # 빈 리스트에 title 추가

    date = soup.select('.t11')[0].text  # select로 class명을 추출해올때는 '.class명'    
    news_detail.append(date) # 기사입력날짜(date) 추가

    _text = soup.select('#articleBodyContents')[0].get_text().replace('\n'," ")
    btext = _text.replace('// flash 오류를 우회하기 위한 함수 추가 function _flash_removeCallback() {}',"")
    news_detail.append(btext.rstrip()) # 기사 본문(btext) 추가

    news_detail.append(n_url)

    return news_detail



# excel_make함수 - 엑셀로 결과 저장

# txt파일로 저장된것 -> csv형식으로 불러와서 data변수에 저장 -> data변수에 columns명을 주고 엑셀파일로 저장

def excel_make():
    
    data = pd.read_csv(RESULT_PATH+'contents_text.txt',sep='\t',header=None, error_bad_lines=False)
    data.columns = ['years','title','contents','link']
    print(data)

    xlsx_outputFileName = '%s-%s-%s %s시 %s분 %s초 result.xlsx' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    data.to_excel(RESULT_PATH+xlsx_outputFileName, encoding='utf-8')




# main함수

def main():
    maxpage = input("최대 출력할 페이지수 입력하시오: ")
    query = input("검색어 입력: ")
    crawler(maxpage,query) 
    
main()




# 참고: https://bumcrush.tistory.com/155







