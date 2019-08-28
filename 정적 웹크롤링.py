### 정적 웹 크롤링 ###


# 연습1 - 네이버 영화 랭킹 페이지에서 영화 목록 가져오기

import urllib.request 
from urllib.request import urlopen 
from bs4 import BeautifulSoup

soup = BeautifulSoup(urllib.request.urlopen('http://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20161120').read(),'html.parser')

''' 웹페이지의 html 구조를 먼저 파악(F12)
하나씩 다 눌러보지 말고, 내가 스크래핑하고자 하는 내용들에 대해 '검사' 누르기 '''


'영화 제목은 div tag 의 tit5를 속성으로 가진 항목들에 포함되어 있으므로'

res = soup.find_all('div', 'tit5')
print(res)

------------------------------------------------------------------------------------------

# 연습2 - 랭킹 소스 에서 테이블 추출

fp = urllib.request.urlopen('https://www.acmicpc.net/ranklist')
source = fp.read()
fp.close()

soup = BeautifulSoup(source)

table = soup.find(id="ranklist")

print(table)


''' table의 tbody 내에 있는 모든 tr을 리스트로 반환
    tr내의 td에 순위정보가 담겨있음 '''

trs = table.tbody.find_all('tr')

for tr in trs[:10] :
    tds = tr.find_all('td')
    rank = tds[0].string
    user_id = tds[1].a.span.string
    print(rank, user_id)

'각각의 user_id는 링크를 위한 a 태그와 아이디 색상을 위한 span 태그로 감싸져 있으므로'


'나머지정보 모두 출력'

for tr in trs[:10] :
    tds = tr.find_all('td')
    rank = tds[0].int(string.strip())
    user_id = tds[1].a.span.string.strip()
    quote = tds[2].string.strip()
    print(rank, user_id)

'strip은 좌우 공백 제거를 위한 것'


'출력한 것을 ans라는 리스트로 저장'

ans = []

for tr in trs[:10] :
    tds = tr.find_all('td')
    rank = tds[0].int(string.strip())
    user_id = tds[1].a.span.string.strip()
    quote = tds[2].string.strip()
    ans.append({rank:rank, user_id:user_id, quote:quote})

print(ans)


------------------------------------------------------------------------------------

# 연습3 - 네이버 뉴스기사를 모듈로 크롤링하기

URL = 'http://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=103&oid=055'\
      '&aid=0000445667'

# 크롤링 함수

'본문 내용은 id가 articleBodyContents인 div클래스 안에 담겨 있음'
'텍스트요소만 뽑아서 문자열로 치환'

def get_text(URL):
    source = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source, 'lxml', from_encoding = 'utf-8')
    text = ''
    for item in soup.find_all('div',id = 'articleBodyContents'):
        text = text + str(item.find_all(text=True))
    return text


# 텍스트 정제 - 영어, 특수기호 모두 제거

text = get_text(URL)

import re

def clean_text(text):
    cleaned_text = re.sub('[a-zA-Z]','',text)
    cleaned_text = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]',
                          '', cleaned_text)
    return cleaned_text

------------------------------------------------------------------------------------

# 연습4 - 네이버 실시간 검색어 추출

from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("https://www.naver.com/").read()
soup = BeautifulSoup(html, "html.parser")
myurl = soup.select('span.ah_k')  # span 태그중 class가 ah_k 인 것만 가져오기
cnt = 0  # 횟수를 세기위한 변수

for j in myurl:
    cnt +=1
    print(str(cnt) + "." + j.text)
    if cnt == 20:
        break

 '''20위까지만 추출할 것이므로'''


 -------------------------------------------------------------------------------

# 연습5 - 특정키워드를 포함하는 신문기사 웹크롤링


import sys
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote

'''urlopen 대신 quote를 사용하는 이유는 인자로 사용되는 URL주소(이하 타겟 주소)에 한글(UTF_8)이 포함되었을 때
이를 아스키(ASCII)형식으로 바꿔주기 위한 함수 이기 때문'''


# 파싱 할 해당 기사페이지의 url패턴을 찾는 것이 우선
# 페이지를 넘길때마다 'p'값이 15씩 더해짐
# url 쪼개기


url_page_num = "http://www.donga.com/news/search?p="
url_keyword = "&query="
url_rest = "&check_news=1&more=1&sorting=3&search_date=1&v1=&v2=&range=3"


# 타겟주소를 결합하여 사용 - 메인함수

def main(argv):
    if len(argv) != 4:
        print("python [모듈이름] [키워드] [가져올페이지숫자] [결과파일명]")
        return
    keyword = argv[1]
    page_num = int(argv[2])
    output_file_name = argv[3]
    target_URL = url_page_num + url_keyword \ 
                 + quote(keyword) + url_rest
    output_file = open(output_file_name, 'w')
    get_link_from_news_title(page_num, target_URL, output_file)
    output_file.close()


if __name__ == '__main__':
    main(sys.argv)


def get_link_from_news_title(page_num, URL, output_file):
    for i in range(page_num):
        current_page_num = 1 + i*15
        position = URL.index('=')
        URL_with_page_num = URL[: position+1] + str(current_page_num) \
                            + URL[position+1 :]
        source_code_from_URL = urllib.request.urlopen(URL_with_page_num)
        soup = BeautifulSoup(source_code_from_URL, 'lxml',from_encoding='utf-8')

        for title in soup.find_all('p', 'tit'):
            title_link = title.select('a')
            article_URL = title_link[0]['href']
            get_text(article_URL, output_file)


''' 인자로 받은 url에서 첫번째로 '='문자가 나오는 위치를 position에 할당,
해당 position 뒤에 current_page_num을 스트링으로 변환 후 삽입 '''
        
''' 페이지 구조 파악 후 기사의 제목 부분을 파싱 '''


def get_text(URL, output_file):
    source_code_from_url = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_url, 'lxml', from_encoding='utf-8')
    content_of_article = soup.select('div.article_txt')
    for item in content_of_article:
        string_item = str(item.find_all(text=True))
        output_file.write(string_item)
 


참고: https://yoonpunk.tistory.com/6

 

