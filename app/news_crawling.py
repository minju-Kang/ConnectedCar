
from typing import Text
from bs4 import BeautifulSoup
from pprint import pprint
from django.shortcuts import render
import requests

def news():
    news_link = "https://www.yna.co.kr/theme/exclusive"
    news_html = requests.get(news_link)

    news_soup = BeautifulSoup(news_html.text, 'html.parser')        

    news_data1 = news_soup.find('ul', {'list'})
    news1 = news_data1.find_all('a', {'class' : 'tit-wrap'})


    newslist = []
    for headline in news1:
        newslist.append(headline.text.strip())
        #print(headline.text.strip())    #얘를 한개씩 CONTEXTS 딕셔너리에 넣어햐 하나?

    newslink = news_soup.find_all('a', {'tit-wrap'})
    newslinklist = []

    for a in newslink:
        href = a.attrs['href']
        newslinklist.append(href)


    context_new = {}
    context_new = {
        'newslist': newslist,
        'newslinklist': newslinklist
    }
    return context_new

#print(news1)

#for headline in news1:
 #   print(headline.text.strip())    #얘를 한개씩 CONTEXTS 딕셔너리에 넣어햐 하나?

