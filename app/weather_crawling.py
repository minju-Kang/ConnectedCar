
from bs4 import BeautifulSoup
from pprint import pprint
from django.shortcuts import render
import requests


def weather():
    #나중에 gps정보 받아와서 link 스트링에 지역명 추가하기
    link = "https://search.naver.com/search.naver?query=" + "여기 날씨"
    html = requests.get(link)

    #pprint(html.text)

    soup = BeautifulSoup(html.text, 'html.parser')

    print()
    print()

    data1 = soup.find('div', {'class': 'weather_box'})

    address = data1.find('span', {'class':'btn_select'}).text
 

    currenttemp = data1.find('span',{'class': 'todaytemp'}).text
   

    data3 = soup.find('div', {'class': 'main_info'})
    weather = data3.find('p',{'class': 'cast_txt'}).text
  

    data2 = data1.findAll('dd')
    dust = data2[0].find('span', {'class':'num'}).text
    ultra_dust = data2[1].find('span', {'class':'num'}).text
    ozone = data2[2].find('span', {'class':'num'}).text

    context_new = {
        'address' : address,
        'temp': currenttemp,
        'weather': weather,
        'dust': dust,
        'ultra_dust': ultra_dust
    }

    return context_new

    #printList = address + "\n" + currenttemp + "\n" + weather + "\n" + dust+"\n"+ultra_dust+"\n"+ozone 
    #print(printList)