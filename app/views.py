# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from bs4 import BeautifulSoup
from pprint import pprint
import requests
from app.models import UserSettings
from app.forms import SettingForm


@login_required(login_url="/login/")
def index(request):

      #나중에 gps정보 받아와서 link 스트링에 지역명 추가하기
    link = "https://search.naver.com/search.naver?query=" + "날씨"
    html = requests.get(link)

    #pprint(html.text)

    soup = BeautifulSoup(html.text, 'html.parser')

    data1 = soup.find('div', {'class': 'weather_box'})

    address = data1.find('span', {'class':'btn_select'}).text
    print('현재 위치: '+address) 

    currenttemp = data1.find('span',{'class': 'todaytemp'}).text
    print('현재 온도: '+currenttemp+'℃')


    data3 = soup.find('div', {'class': 'main_info'})
    weather = data3.find('p',{'class': 'cast_txt'}).text
    print('현재 날씨:' + weather)

    data2 = data1.findAll('dd')
    dust = data2[0].find('span', {'class':'num'}).text
    ultra_dust = data2[1].find('span', {'class':'num'}).text
    ozone = data2[2].find('span', {'class':'num'}).text

    print('현재 미세먼지: '+dust)
    print('현재 초미세먼지: '+ultra_dust)
    print('현재 오존지수: '+ozone)
   # return render(request, 'includes/widget.html', {'address': address, 'currenttemp': currenttemp})


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


    context = {}
    context['segment'] = 'index'
    context = {
        'address' : address,
        'temp': currenttemp,
        'weather': weather,
        'dust': dust,
        'ultra_dust': ultra_dust,
        'newslist': newslist,
        'newslinklist': newslinklist
    }

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context,request))
   

    #html_template = loader.get_template( 'index.html' )
    #return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def save(request):
    if request.method == 'POST':
        instance = get_object_or_404(UserSettings, name=request.user.username)
        setting_form = SettingForm(request.POST)

        if setting_form.is_valid():
            if setting_form.cleaned_data['news'] == 'T':
                instance.wNews = 1
                request.session['news'] = 1
            if setting_form.cleaned_data['stock'] == 'T':
                instance.wStock = 1
                request.session['stock'] = 1
            if setting_form.cleaned_data['weather'] == 'T':
                instance.wWeather = 1
                request.session['weather'] = 1
            if setting_form.cleaned_data['mail'] == 'T':
                instance.wMail = 1
                request.session['mail'] = 1
            if setting_form.cleaned_data['calendar'] == 'T':
                instance.wCalendar = 1
                request.session['calendar'] = 1

            instance.save()

    return render(request, 'page-user.html')


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))
