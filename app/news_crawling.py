
from typing import Text
from bs4 import BeautifulSoup
from pprint import pprint
from django.shortcuts import render
import requests


news_link = "https://www.yna.co.kr/theme/exclusive"
news_html = requests.get(news_link)


news_soup = BeautifulSoup(news_html.text, 'html.parser')

news_data1 = news_soup.find('ul', {'list'})
news1 = news_data1.find_all('a', {'class' : 'tit-wrap'})

linklist = news_soup.find_all('a', {'tit-wrap'})
print(linklist)

for a in linklist:
    href = a.attrs['href']
    print(href)



#print(news1)

#for headline in news1:
 #   print(headline.text.strip())    #얘를 한개씩 CONTEXTS 딕셔너리에 넣어햐 하나?


