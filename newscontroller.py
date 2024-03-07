import requests
from bs4 import BeautifulSoup as BS
import time

from DBmanager import DBmanager


def read_news(url,time):
    response = [url, time]
    r = requests.get(url)
    soup = BS(r.text, 'html.parser')
    theme1 = soup.find_all("h3")
    if len(theme1) > 1:
        response.append(str(theme1[1]).replace("<h3>","").replace("</h3>",""))
    else:
        return 0
    print(response)
    #db = DBmanager()
    #db.add_news(response[0], response[1], response[2], response[3])
    #db.commit()
    return response
def check_news():
    nocheck = []
    while True:

        url = "https://www.disclosure.ru/rus/corpnews/index.shtml"
        r = requests.get(url)
        soup = BS(r.text, 'html.parser')
        teme = soup.find_all("table")
        soup = BS(str(teme[0]), 'html.parser')
        teme1 = soup.find_all("a")

        spisok = []
        spisok_time = []
        for i in teme1:
            if "news.shtml?newsisn" in  i['href']:
                soup = BS(str(i), 'html.parser')
                news_date = str(soup.find_all("b")[0]).replace("<b>","").replace("</b>","")
                spisok_time.append(news_date)
                spisok.append("https://www.disclosure.ru/rus/corpnews/"+i['href'])
        print(spisok)
        print(spisok_time)
        for i in range(len(spisok)):
            read_news(spisok[i], spisok_time[i])
        time.sleep(120)
def check_company():
    nocheck = []
    while True:

        url = "http://www.disclosure.ru/issuer/index.shtml"
        r = requests.get(url)
        soup = BS(r.text, 'html.parser')
        teme = soup.find_all("table")
        soup = BS(str(teme[0]), 'html.parser')
        teme1 = soup.find_all("a")
        #print(teme)
        spisok = []
        spisok_time = []
        for i in teme1:

            soup = BS(str(i), 'html.parser')
            if len(soup.find_all("b")) > 0:
                news_date = str(soup.find_all("b")[0]).replace("<b>","").replace("</b>","")
                spisok_time.append(news_date.replace("\r","").replace("\n","")[1:])
                #spisok.append("https://www.disclosure.ru/rus/corpnews/"+i['href'])
        print(spisok)
        print(spisok_time)
        break
        #for i in range(len(spisok)):
        #   read_news(spisok[i], spisok_time[i])
        #time.sleep(120)
check_company()

#check_news()