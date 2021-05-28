
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

    data1 = soup.find('div', {'class': 'weather_box'})

    address = data1.find('span', {'class':'btn_select'}).text
 

    currenttemp = data1.find('span',{'class': 'todaytemp'}).text
   

    data3 = soup.find('div', {'class': 'main_info'})
    weather = data3.find('p',{'class': 'cast_txt'}).text
    cnt = 0
    for ch in weather:
        cnt = cnt+1
        if ch == "어":
            img_text = weather[0:cnt-3]
   
    img_src=""
    if img_text == "맑음" or img_text == "구름조금":
        print("날씨", img_text)
        img_src = "https://image.flaticon.com/icons/png/128/869/869869.png"
    elif img_text == "구름많음" or img_text == "흐림":
        img_src = "https://image.flaticon.com/icons/png/128/494/494435.png"
    elif img_text == "약한비" or img_text =="비" or img_text =="강한비" or img_text =="소나기":
        img_src = "https://image.flaticon.com/icons/png/128/3313/3313966.png"
    elif img_text == "약한눈" or img_text =="눈" or img_text =="강한눈" or img_text =="진눈깨비" or img_text =="소낙눈":
        img_src = "https://image.flaticon.com/icons/png/128/3026/3026312.png"
    else:
        img_src = "https://image.flaticon.com/icons/png/128/869/869869.png"


    data2 = data1.findAll('dd')
    dust = data2[0].find('span', {'class':'num'}).text
    ultra_dust = data2[1].find('span', {'class':'num'}).text
    cnt =0
    for ch in dust:
        cnt = cnt+1
        if ch == "㎍":
            dust_num = dust[0:cnt-1]
    cnt=0
    for ch in ultra_dust:
        cnt = cnt+1
        if ch == "㎍":
            ultra_dust_num = ultra_dust[0:cnt-1]
   
    dust_state = ""
    ultra_dust_state = ""
    dust_src = ""
    ultra_dust_src = ""
    if int(dust_num) >=0 and int(dust_num)<=30:
        dust_state = "좋음"
        dust_src = "https://image.flaticon.com/icons/png/128/725/725107.png"
    elif int(dust_num) > 30 and int(dust_num) <=80:
        dust_state = "보통"
        dust_src = "https://image.flaticon.com/icons/png/128/725/725105.png"
    elif int(dust_num) > 80 and int(dust_num) <=150:
        dust_state = "나쁨"
        dust_src = "https://image.flaticon.com/icons/png/128/725/725085.png"
    elif int(dust_num) <150:
        dust_state = "매우나쁨"
        dust_src = "https://image.flaticon.com/icons/png/128/725/725099.png"
    
    if int(ultra_dust_num) >=0 and int(ultra_dust_num)<=15:
        ultra_dust_state = "좋음"
        ultra_dust_src = "https://image.flaticon.com/icons/png/128/725/725107.png"
    elif int(ultra_dust_num) > 15 and int(ultra_dust_num) <=35:
        ultra_dust_state = "보통"
        ultra_dust_src = "https://image.flaticon.com/icons/png/128/725/725105.png"
    elif int(ultra_dust_num) > 35 and int(ultra_dust_num) <=75:
        ultra_dust_state = "나쁨"
        ultra_dust_src = "https://image.flaticon.com/icons/png/128/725/725085.png"
    elif int(ultra_dust_num) <75:
        ultra_dust_state = "매우나쁨"
        ultra_dust_src = "https://image.flaticon.com/icons/png/128/725/725099.png"

    context_new = {
        'address' : address,
        'temp': currenttemp,
        'weather_state': weather,
        'dust': dust_state,
        'ultra_dust': ultra_dust_state,
        'img_src' : img_src,
        'dust_src': dust_src,
        'ultra_dust_src' : ultra_dust_src
    }

    return context_new

    #printList = address + "\n" + currenttemp + "\n" + weather + "\n" + dust+"\n"+ultra_dust+"\n"+ozone 
    #print(printList)