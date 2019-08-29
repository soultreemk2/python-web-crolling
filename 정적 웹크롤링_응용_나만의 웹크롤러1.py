## 정적웹크롤링_응용 ##


### 나만의 웹 크롤러 만들기 ###


'''

목표: 네이버 검색창에 검색한 단어와 관련된 기사들을 추출하는 것


<크롤링 할 것>

기사 제목
신문사  
해당 기사 하이퍼링크


<프로그램 돌아가는 방식>

1. main함수 - 사용자가 입력한 값(최대 검색 페이지수, 검색어)을 받아 crawler함수로 넘김
2. crawler 함수 - 크롤링 할 내용들 추출(기사제목,신문사,URL)
3. 웹크롤링 결과 저장 (리스트 -> 딕셔너리 -> data frame -> 엑셀)


'''



#### 크롤러 함수 만드는 과정 ####

# 필요한 라이브러리 import

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

RESULT_PATH = 'C:/git_project/' #크롤링 결과를 저장할 폴더 경로
now = datetime.now() #최종 저장파일이름을 현 시간으로 저장하기

    

# crawler 함수 정의

def crawler(maxpage,query):
    
    page = 1

    # 빈 리스트 만들기 - 제목,url,신문사 저장
    
    news_title = []
    news_url = []
    news_source = []
            
    while page <= int(maxpage):

        maxpage_t = (int(page)-1)*10+1 
        url = "https://search.naver.com/search.naver?&where=news&query=" + query + " &start=" + str(maxpage_t)
    
        response = requests.get(url)
        
        html = response.text  

        soup = BeautifulSoup(html, 'html.parser') # url 파싱
        
        atags = soup.select('._sp_each_title')
        
        for atag in atags:
            news_title.append(atag.text)   # 기사 제목 추출해서 리스트에 담기
            news_url.append(atag['href'])  # 기사 url 추출해서 리스트에 담기

        for source in soup.select('._sp_each_source'):
            news_source.append(source.text) # 기사의 신문사 추출해서 리스트에 담기

        page += 1  # 다음페이지로 넘겨서 똑같은 작업 반복
        
    # 기사 제목/url/신문사는 각각 news_title/news_url/news_source 리스트에 담김
    # 모든 리스트를 딕셔너리로 변경 -> 딕셔너리는 데이터프레임으로 변경 -> 엑셀로 저장

    result = {"title" : news_title, "url" : news_url, "source" : news_source}
    
    df = pd.DataFrame(result)
        
    outputFileName = '%s-%s-%s  %s시 %s분 %s초 검색.xlsx' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    df.to_excel(RESULT_PATH+outputFileName,sheet_name='sheet1')



# main함수 정의 - main함수에서 사용자로부터 값을 받아와 crawler함수로 넘겨준다


def main():
    maxpage = input("최대 출력할 페이지수 입력하시오: ")
    query = input("검색어 입력: ")
    crawler(maxpage,query)
    
main()



