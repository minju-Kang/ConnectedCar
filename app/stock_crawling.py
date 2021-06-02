
from typing import Text
from bs4 import BeautifulSoup
from pprint import pprint
from django.shortcuts import render
import requests

def stock():
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}

    stock_link = "https://m.stock.naver.com/"
    stock_html = requests.get(stock_link, headers=headers)

    #1. 코스피
    stock_soup = BeautifulSoup(stock_html.text, 'html.parser')
    stock_data1 = stock_soup.find('ul', {'list_chart'})

    gap_stock_soup = stock_soup
    for em in gap_stock_soup("em"):
        em.decompose()
    gap_stocK_data1 = gap_stock_soup.find('ul', {'list_chart'})
    stock1 = stock_data1.find('li', {'class' : '_kospi'})
    gap_stock1 = gap_stocK_data1.find('li', {'class' : '_kospi'})

    kospi_price = stock1.find('span', {'stock_price stock_up'}).text   #가격 나옴

    kospi_gap_price = gap_stock1.find('span', {'gap_price'}).text #가격변동
    kospi_gap_rate = stock1.find('span', {'gap_rate'}).text #퍼센티지 변동 및 상승하락 여부
    kospi_shape = kospi_gap_rate[0]
    kospi_shape_imgsrc = ""
    if kospi_shape == '+':
        kospi_shape_imgsrc = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Armed_forces_red_triangle.svg/1200px-Armed_forces_red_triangle.svg.png"
    else:
        kospi_shape_imgsrc = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Blue_triangle.svg/1152px-Blue_triangle.svg.png"    

    imgsrc = stock1.find_all('img', {'_img_chart'}) #그래프이미지소스
    for img in imgsrc:
        kospi_imgsrc = img.attrs['src']
    stock_soup = BeautifulSoup(stock_html.text, 'html.parser')
    stock_data1 = stock_soup.find('ul', {'list_chart'})
    stock1 = stock_data1.find('li', {'class' : '_kospi'})
    kospi_trend = stock1.find('li',{'stock_up'})
    kospi_trend_pe = kospi_trend.find('span', {'data'}).text #개인
    kospi_trend = stock1.find('li',{'stock_dn'})
    kospi_trend_fo = kospi_trend.find('span', {'data'}).text #외인
    kospi_trend = (stock1.find_all('li',{'stock_up'}))[0].text
    kospi_trend_co = kospi_trend[3:len(kospi_trend)]  #기관


    #2. 코스닥
    stock_soup = BeautifulSoup(stock_html.text, 'html.parser')
    stock_data2 = stock_soup.find('ul', {'list_chart'})

    gap_stock_soup = stock_soup
    for em in gap_stock_soup("em"):
        em.decompose()
    gap_stocK_data2 = gap_stock_soup.find('ul', {'list_chart'})
    stock2 = stock_data2.find('li', {'class' : '_kosdaq'})
    gap_stock2 = gap_stocK_data2.find('li', {'class' : '_kosdaq'})

    kosdaq_price = stock2.find('span', {'stock_price stock_up'}).text   #가격 나옴


    kosdaq_gap_price = gap_stock2.find('span', {'gap_price'}).text #가격변동
    kosdaq_gap_rate = stock2.find('span', {'gap_rate'}).text #퍼센티지 변동 및 상승하락 여부
    kosdaq_shape = kosdaq_gap_rate[0]
    kosdaq_shape_imgsrc = ""
    if kosdaq_shape == '+':
        kosdaq_shape_imgsrc = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Armed_forces_red_triangle.svg/1200px-Armed_forces_red_triangle.svg.png"
    else:
        kosdaq_shape_imgsrc = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Blue_triangle.svg/1152px-Blue_triangle.svg.png" 

    imgsrc = stock2.find_all('img', {'_img_chart'}) #그래프이미지소스
    for img in imgsrc:
        kosdaq_imgsrc = img.attrs['src']
    stock_soup = BeautifulSoup(stock_html.text, 'html.parser')
    stock_data2 = stock_soup.find('ul', {'list_chart'})
    stock2 = stock_data2.find('li', {'class' : '_kosdaq'})
    kosdaq_trend = stock2.find('li',{'stock_dn'})
    kosdaq_trend_pe = kosdaq_trend.find('span', {'data'}).text #개인

    kosdaq_trend = stock2.find('li',{'stock_up'})
    kosdaq_trend_fo = kosdaq_trend.find('span', {'data'}).text #외인
    kosdaq_trend = (stock2.find_all('li',{'stock_up'}))[1].text

    kosdaq_trend_co = kosdaq_trend[3:len(kosdaq_trend)] #기관
    


    kospi_data = [] #코스피 데이터
    kospi_data.append(kospi_price)
    kospi_data.append(kospi_gap_price)
    kospi_data.append(kospi_gap_rate)
    kospi_data.append(kospi_imgsrc)
    kospi_data.append(kospi_trend_pe)
    kospi_data.append(kospi_trend_fo)
    kospi_data.append(kospi_trend_co)
    kospi_data.append(kospi_shape_imgsrc)

    kosdaq_data = [] #코스닥 데이터
    kosdaq_data.append(kosdaq_price)
    kosdaq_data.append(kosdaq_gap_price)
    kosdaq_data.append(kosdaq_gap_rate)
    kosdaq_data.append(kosdaq_imgsrc)
    kosdaq_data.append(kosdaq_trend_pe)
    kosdaq_data.append(kosdaq_trend_fo)
    kosdaq_data.append(kosdaq_trend_co)
    kosdaq_data.append(kosdaq_shape_imgsrc)

    #인기 검색 종목
    stock_link = "https://finance.naver.com/"
    stock_html = requests.get(stock_link, headers=headers)

    stock_soup = BeautifulSoup(stock_html.text, 'html.parser')
    #lanking_data = stock_soup.find('div', {'ct_box trend_box _home_trend_wrapper'})
    lanking_data = stock_soup.find('div', {'class':'aside_area aside_popular'})
    lanking_data1 = lanking_data.find('table', {'class':'tbl_home'})
    lanking_data2 = lanking_data1.find_all('th', {'scope': 'row'})
    lanking_data_text = [] #랭킹 텍스트
    for data in lanking_data2:
        lanking_data_text.append(data.text)

    stock_soup = BeautifulSoup(stock_html.text, 'html.parser')
    #lanking_data = stock_soup.find('div', {'ct_box trend_box _home_trend_wrapper'})
    lanking_data = stock_soup.find('div', {'class':'aside_area aside_popular'})
    lanking_data1 = lanking_data.find('table', {'class':'tbl_home'})
    lanking_data_price = [] #랭킹 가격
    lanking_data2 = stock_soup.select_one("#container > div.aside > div.group_aside > div.aside_area.aside_popular > table > tbody > tr:nth-child(1) > td:nth-child(2)").text
    lanking_data_price.append(lanking_data2)
    lanking_data2 = stock_soup.select_one("#container > div.aside > div.group_aside > div.aside_area.aside_popular > table > tbody > tr:nth-child(2) > td:nth-child(2)").text
    lanking_data_price.append(lanking_data2)
    lanking_data2 = stock_soup.select_one("#container > div.aside > div.group_aside > div.aside_area.aside_popular > table > tbody > tr:nth-child(3) > td:nth-child(2)").text
    lanking_data_price.append(lanking_data2)
    lanking_data2 = stock_soup.select_one("#container > div.aside > div.group_aside > div.aside_area.aside_popular > table > tbody > tr:nth-child(4) > td:nth-child(2)").text
    lanking_data_price.append(lanking_data2)
    lanking_data2 = stock_soup.select_one("#container > div.aside > div.group_aside > div.aside_area.aside_popular > table > tbody > tr:nth-child(5) > td:nth-child(2)").text
    lanking_data_price.append(lanking_data2)
    #container > div.aside > div.group_aside > div.aside_area.aside_popular > table > tbody > tr:nth-child(1) > td:nth-child(2)
    
    

    stock_soup = BeautifulSoup(stock_html.text, 'html.parser')
    lanking_data_gap = []#랭킹갭
    lanking_data3 = stock_soup.select_one("#container > div.aside > div.group_aside > div.aside_area.aside_popular > table > tbody > tr:nth-child(1) > td:nth-child(3) > span").text
    lanking_data_gap.append(lanking_data3)
    lanking_data3 = stock_soup.select_one("#container > div.aside > div.group_aside > div.aside_area.aside_popular > table > tbody > tr:nth-child(2) > td:nth-child(3) > span").text
    lanking_data_gap.append(lanking_data3)
    lanking_data3 = stock_soup.select_one("#container > div.aside > div.group_aside > div.aside_area.aside_popular > table > tbody > tr:nth-child(3) > td:nth-child(3) > span").text
    lanking_data_gap.append(lanking_data3)
    lanking_data3 = stock_soup.select_one("#container > div.aside > div.group_aside > div.aside_area.aside_popular > table > tbody > tr:nth-child(4) > td:nth-child(3) > span").text
    lanking_data_gap.append(lanking_data3)
    lanking_data3 = stock_soup.select_one("#container > div.aside > div.group_aside > div.aside_area.aside_popular > table > tbody > tr:nth-child(5) > td:nth-child(3) > span").text
    lanking_data_gap.append(lanking_data3)

   # lanking_data_gap_rate 
    lanking_shape_src = []
    stock_link = "https://finance.naver.com/main/main.nhn"
    stock_html = requests.get(stock_link, headers=headers)
    stock_soup = BeautifulSoup(stock_html.text, 'html.parser')
    
    here_up = "https://ssl.pstatic.net/imgstock/images/images4/ico_up.gif"
    here_down = "https://ssl.pstatic.net/imgstock/images/images4/ico_down.gif"

    up_link = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Armed_forces_red_triangle.svg/1200px-Armed_forces_red_triangle.svg.png"
    down_link = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Blue_triangle.svg/1152px-Blue_triangle.svg.png"
    #tag = soup.select('img')[0]['btn-title']
    lanking_data4 = stock_soup.select_one("#container > div.aside > div.group_aside > div.aside_area.aside_popular > table > tbody > tr:nth-child(1) > td:nth-child(3)")
    lanking_data5 = lanking_data4.find("img")['src']
    if lanking_data5 == here_up:
        lanking_shape_src.append(up_link)
    else:
        lanking_shape_src.append(down_link)

    lanking_data4 = stock_soup.select_one("#container > div.aside > div.group_aside > div.aside_area.aside_popular > table > tbody > tr:nth-child(2) > td:nth-child(3)")
    lanking_data5 = lanking_data4.find("img")['src']
    if lanking_data5 == here_up:
        lanking_shape_src.append(up_link)
    else:
        lanking_shape_src.append(down_link)

    lanking_data4 = stock_soup.select_one("#container > div.aside > div.group_aside > div.aside_area.aside_popular > table > tbody > tr:nth-child(3) > td:nth-child(3)")
    lanking_data5 = lanking_data4.find("img")['src']
    if lanking_data5 == here_up:
        lanking_shape_src.append(up_link)
    else:
        lanking_shape_src.append(down_link)

    lanking_data4 = stock_soup.select_one("#container > div.aside > div.group_aside > div.aside_area.aside_popular > table > tbody > tr:nth-child(4) > td:nth-child(3)")
    lanking_data5 = lanking_data4.find("img")['src']
    if lanking_data5 == here_up:
        lanking_shape_src.append(up_link)
    else:
        lanking_shape_src.append(down_link)

    lanking_data4 = stock_soup.select_one("#container > div.aside > div.group_aside > div.aside_area.aside_popular > table > tbody > tr:nth-child(5) > td:nth-child(3)")
    lanking_data5 = lanking_data4.find("img")['src']
    if lanking_data5 == here_up:
        lanking_shape_src.append(up_link)
    else:
        lanking_shape_src.append(down_link)
 
   # for data in lanking_data2:
   #     temp = data.find('span').text
   #     lanking_data_gap.append(temp[1:len(temp)])
    print(lanking_shape_src)
    stock_lanking = []
    stock_lanking.append(lanking_data_text)
    stock_lanking.append(lanking_data_price)
    stock_lanking.append(lanking_data_gap)
    stock_lanking.append(lanking_shape_src)
    stock_total = {
        'kospi': kospi_data, #배열
        'kosdaq': kosdaq_data, #배열
        'lanking': stock_lanking #배열 안에 배열
    }

    return stock_total