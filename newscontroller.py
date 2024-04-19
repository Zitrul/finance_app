import requests
from bs4 import BeautifulSoup as BS
import time
#from special_info import comp as companies
import DBmanager
def read_news(url,time):
    desc = ""
    company = ""
    r = requests.get(url)
    soup = BS(r.text, 'html.parser')
    theme1 = soup.find_all("h3")
    if len(theme1) > 1:
        desc = str(theme1[1]).replace("<h3>","").replace("</h3>","")
        n = len(desc)
        #print(desc)
        for j in range(n):
            if desc[n-j-1] == '-':
                #print(n-j-1)
                company = desc[0:n-j-1]
        print(company)
        if company == "":
            return 0


    else:
        return 0
    response = [company,url,desc,time]
    db = DBmanager.DBmanager()
    db.add_news(response[0], response[1], response[2], response[3])
    db.commit()
    return response
def check_news():
    nocheck = []
    while True:
        db = DBmanager.DBmanager()
        links = db.get_link_news()

        #print(links)
        db.commit()
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
                if ("https://www.disclosure.ru/rus/corpnews/"+i['href'],) not in links:
                    soup = BS(str(i), 'html.parser')
                    news_date = str(soup.find_all("b")[0]).replace("<b>","").replace("</b>","")
                    spisok_time.append(news_date)
                    spisok.append("https://www.disclosure.ru/rus/corpnews/"+i['href'])
        print(spisok)
        print(spisok_time)
        for i in range(len(spisok)):
            read_news(spisok[i], spisok_time[i])
        time.sleep(120)
        #for i in range(len(spisok)):
        #   read_news(spisok[i], spisok_time[i])
        #time.sleep(120)
if __name__ == "__main__":
    check_news()
