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


import sys
sys.path.append('\app')
from . import weather_crawling
from . import news_crawling
from . import stock_crawling



@login_required(login_url="/login/")
def index(request):
    context = {}
    context.update(weather_crawling.weather())
    context.update(news_crawling.news())
    context.update(stock_crawling.stock())
    context.update(request.session.__dict__['_session_cache'])
    context['segment'] = 'index'

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
            else:
                instance.wNews = 0
                request.session['news'] = 0
            if setting_form.cleaned_data['stock'] == 'T':
                instance.wStock = 1
                request.session['stock'] = 1
            else:
                instance.wStock = 0
                request.session['stock'] = 0
            if setting_form.cleaned_data['weather'] == 'T':
                instance.wWeather = 1
                request.session['weather'] = 1
            else:
                instance.wWeather = 0
                request.session['weather'] = 0
            if setting_form.cleaned_data['mail'] == 'T':
                instance.wMail = 1
                request.session['mail'] = 1
            else:
                instance.wMail = 0
                request.session['mail'] = 0
            if setting_form.cleaned_data['calendar'] == 'T':
                instance.wCalendar = 1
                request.session['calendar'] = 1
            else:
                instance.wCalendar = 0
                request.session['calendar'] = 0
            instance.save()

    return render(request, 'page-user.html', request.session.__dict__['_session_cache'])


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
