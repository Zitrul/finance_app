import os
import sqlite3
from datetime import datetime, timedelta

import requests
from pyzbar import pyzbar
import cv2
from glob import glob

import DBmanager
from classes import Product

categories = ['Мясная гастрономия', 'Сладости и десерты', 'Сыры', 'Овощи и фрукты', 'Кулинария', 'Выпечка и хлеб',
              'Напитки', 'Замороженные полуфабрикаты', 'Товары для животных', 'Алкоголь', 'Косметика средства гигиены',
              'Молочные продукты', 'Мясо птица', 'Рыба и морепродукты', 'Детское питание', 'Техника', 'Ремонт',
              'Товары для дома', 'Авто', 'Канцтовары', 'Красота и здоровье', 'Досуг и хобби', 'Игрушки', 'Мебель',
              'Детская одежда и обувь', 'Хозтовары', 'Зоотовары', 'Детям и мамам', 'Книги', 'Дача и сад']


def compare(s1, s2):
    words1 = s1.lower().split()
    words2 = s2.lower().split()
    list1 = []
    list2 = []
    count = 0
    for i in words1:
        if len(i) > 4:
            list1.append(i)
    for i in words2:
        if len(i) > 3:
            list2.append(i)
    for words in words1:
        count += list2.count(words)
    a = min(count / (max(len(list1), 1)), 1) * 100 * min(count / max(len(list2), 1), 1)
    return a


def auto_sort(products_to_check):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    product_like = []
    found_flag = 0
    n = len(products_to_check)
    result = []

    for i in range(n):
        result.append(0)
        product_like.append(0)

    for category in categories:
        cursor.execute(f'SELECT product FROM Product_to_compare WHERE type = ?;', [category])
        rows = cursor.fetchall()

        for row in rows:

            for i in range(n):
                check = compare(products_to_check[i].name, row[0])
                if check > result[i] and check > 60:
                    result[i] = check
                    product_like[i] = row[0]
                    products_to_check[i].category = category

        if found_flag != 0:
            break

    print(result)
    print(product_like)
    conn.commit()
    conn.close()

    return products_to_check


def CHECK_CHECKER(auto_change, user_id, file_location):
    url = "https://proverkacheka.com/api/v1/check/get"
    filename = file_location

    img = cv2.imread(filename)
    qrcodes = pyzbar.decode(img)
    print(qrcodes)
    os.remove(filename)
    if len(qrcodes) > 1:
        return "Лишняя информация на чеке"
    if len(qrcodes) == 0:
        return "Нет возможности считать QR"
    qrcodeData = qrcodes[0].data.decode('utf-8')

    if "fn=" not in qrcodeData:
        return "Bad QR1"
    data = {
        "token": "26100.4sb0EVJFGzDVYmQ9w",
        "qrraw": qrcodeData,
    }

    r = requests.post(url, data=data)
    if r == "":
        return "Bad QR2"
    check_1 = eval(r.text)
    print(check_1)
    print(qrcodeData)
    # check_1 = {"code":1,"first":0,"data":{"json":{"code":3,"user":"ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ \"ТД СИГМА-ТОРГ\"","items":[{"nds":2,"sum":27400,"name":"9 шт ОРИГ Стрипсы кур фил","price":27400,"quantity":1,"paymentType":4,"productType":1},{"nds":1,"sum":3100,"name":"Соус Чесночный","price":3100,"quantity":1,"paymentType":4,"productType":1},{"nds":2,"sum":20400,"name":"БоксМастер из тостера ОРИГ СЛ","price":20400,"quantity":1,"paymentType":4,"productType":1}],"nds10":4346,"nds18":517,"fnsUrl":"www.nalog.ru","region":"77","userInn":"7705944498  ","dateTime":"2021-07-21T20:25:00","kktRegId":"0004193146019089    ","metadata":{"id":3806554194634009600,"ofdId":"ofd7","address":"125009,Россия,Г.Москва,,,,,Манежная пл элем. улично-дорожн.сети,,д. 1,,,к. 2 стр,","subtype":"receipt","receiveDate":"2021-07-21T17:25:10Z"},"operator":"Сафаров Музаффар","totalSum":50900,"creditSum":0,"numberKkt":"009002203","fiscalSign":1189168989,"prepaidSum":0,"retailPlace":"ресторан KFC, уровень -3","shiftNumber":102,"cashTotalSum":0,"provisionSum":0,"ecashTotalSum":50900,"operationType":1,"redefine_mask":10,"requestNumber":238,"fiscalDriveNumber":"9285440300346590","messageFiscalSign":9.297253059366777e+18,"appliedTaxationType":1,"fiscalDocumentNumber":13614,"fiscalDocumentFormatVer":2},"html":"<table class=\"b-check_table table\"><tbody><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ \"ТД СИГМА-ТОРГ\"<\/td><\/tr><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">125009, Россия, Г.Москва, Манежная пл элем. улично-дорожн.сети, д. 1, к. 2 стр<\/td><\/tr><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">ИНН 7705944498  <\/td><\/tr><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">&nbsp;<\/td><\/tr><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">21.07.2021 20:25<\/td><\/tr><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">Чек № 238<\/td><\/tr><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">Смена № 102<\/td><\/tr><tr class=\"b-check_vblock-middle b-check_center\"><td colspan=\"5\">Кассир Сафаров Музаффар<\/td><\/tr><tr class=\"b-check_vblock-last b-check_center\"><td colspan=\"5\">Приход<\/td><\/tr><tr><td><strong>№<\/strong><\/td><td><strong>Название<\/strong><\/td><td><strong>Цена<\/strong><\/td><td><strong>Кол.<\/strong><\/td><td><strong>Сумма<\/strong><\/td><\/tr><tr class=\"b-check_item\"><td>1<\/td><td>9 шт ОРИГ Стрипсы кур фил<\/td><td>274.00<\/td><td>1<\/td><td>274.00<\/td><\/tr><tr class=\"b-check_item\"><td>2<\/td><td>Соус Чесночный<\/td><td>31.00<\/td><td>1<\/td><td>31.00<\/td><\/tr><tr class=\"b-check_item\"><td>3<\/td><td>БоксМастер из тостера ОРИГ СЛ<\/td><td>204.00<\/td><td>1<\/td><td>204.00<\/td><\/tr><tr class=\"b-check_vblock-first\"><td colspan=\"3\" class=\"b-check_itogo\">ИТОГО:<\/td><td><\/td><td class=\"b-check_itogo\">509.00<\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"3\">Наличные<\/td><td><\/td><td>0.00<\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"3\">Карта<\/td><td><\/td><td>509.00<\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"3\">НДС итога чека со ставкой 20%<\/td><td><\/td><td>5.17<\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"3\">НДС итога чека со ставкой 10%<\/td><td><\/td><td>43.46<\/td><\/tr><tr class=\"b-check_vblock-last\"><td colspan=\"5\">ВИД НАЛОГООБЛОЖЕНИЯ: ОСН<\/td><\/tr><tr class=\"b-check_vblock-first\"><td colspan=\"5\">РЕГ.НОМЕР ККТ: 0004193146019089    <\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"5\">ЗАВОД. №: <\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"5\">ФН: 9285440300346590<\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"5\">ФД: 13614<\/td><\/tr><tr class=\"b-check_vblock-middle\"><td colspan=\"5\">ФПД#: 1189168989<\/td><\/tr><tr class=\"b-check_vblock-last\"><td colspan=\"5\" class=\"b-check_center\"><img src=\"\/qrcode\/generate?text=t%3D20210721T2025%26s%3D509.00%26fn%3D9285440300346590%26i%3D13614%26fp%3D1189168989%26n%3D1\" alt=\"QR код чека\" width=\"35%\" loading=\"lazy\" decoding=\"async\"><\/td><\/tr><\/tbody><\/table>"},"request":{"qrurl":"","qrfile":"","qrraw":"t=20210721t2025&s=509.00&fn=9285440300346590&i=13614&fp=1189168989&n=1","manual":{"fn":"9285440300346590","fd":"13614","fp":"1189168989","check_time":"20210721t2025","type":"1","sum":"509"}}}
    data_s_cheka = check_1["data"]["json"]["items"]
    product_list = dict()
    Product_List = []
    for i in data_s_cheka:
        product = Product(name=i["name"], amount= i["price"] / 100 * i["quantity"],currency="RUB", category="Остальное")
        Product_List.append(product)
    if auto_change:
        Product_List = auto_sort(Product_List)
    print(Product_List)
    db = DBmanager.DBmanager()
    db.add_products(Product_List, user_id)
    db.commit()
    return "QR code прочитан"
    # print(check_data["data"]["json"]["items"])


def auto_sort(products_to_check):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    product_like = []
    found_flag = 0
    n = len(products_to_check)
    result = []

    for i in range(n):
        result.append(0)
        product_like.append(0)

    for category in categories:
        cursor.execute(f'SELECT product FROM Product_to_compare WHERE type = ?;', [category])
        rows = cursor.fetchall()

        for row in rows:

            for i in range(n):
                check = compare(products_to_check[i].name, row[0])
                if check > result[i] and check > 60:
                    result[i] = check
                    product_like[i] = row[0]
                    products_to_check[i].category = category

        if found_flag != 0:
            break
    print(result)
    print(product_like)
    conn.commit()
    conn.close()

    return products_to_check


def add_by_qr_info(auto_change, user_id, qr_data):
    url = "https://proverkacheka.com/api/v1/check/get"
    data = {
        "token": "26100.4sb0EVJFGzDVYmQ9w",
        "qrraw": qr_data,
    }
    r = requests.post(url, data=data)
    if r == "":
        return "Bad QR2"
    check_1 = eval(r.text)
    data_s_cheka = check_1["data"]["json"]["items"]
    Product_List = []
    for i in data_s_cheka:
        product = Product(name=i["name"], amount= i["price"] / 100 * i["quantity"],currency="RUB", category="Остальное")
        Product_List.append(product)
    if auto_change:
        Product_List = auto_sort(Product_List)
    print(Product_List)
    db = DBmanager.DBmanager()
    db.add_products(Product_List, user_id)
    db.commit()
    return "QR code прочитан"
def get_history(ticket, date_start, date_end):
    result = dict()
    date_end_copy = date_end
    date_start = datetime.strptime(date_start, "%Y-%m-%d").date()
    date_end = datetime.strptime(date_end, "%Y-%m-%d").date()
    days = max((date_end - date_start).days, 1)
    date_end_dt = datetime.strptime(date_end_copy, "%Y-%m-%d")
    f = 1
    for day in range(0, days):
        date_now = (date_start + timedelta(days=day)).strftime("%Y-%m-%d")
        url = f'https://iss.moex.com/iss/history/engines/stock/markets/shares/securities/{ticket}/securities.json?from={date_now}&tradingsession=1'
        info = requests.get(url).json()
        #print(info)
        data = info["history"]["data"]
        for inform in data:
            date1 = datetime.strptime(inform[1], "%Y-%m-%d")
            if date1 <= date_end_dt:
                result[inform[1]] = inform[6]
            else:
                print(date1, date_end_dt)
                f = 0
                break
        if f == 0:
            break
    return result
