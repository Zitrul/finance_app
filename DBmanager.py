from datetime import datetime

import pymysql.cursors


class DBmanager:
    def __init__(self):

        self.conn = pymysql.connect(host="188.244.45.227",
                                    port=3306,
                                    user="sigma",
                                    password="j$sdjk!53",
                                    db="main_db",
                                    charset='utf8',
                                    )
        self.cur = self.conn.cursor()

    def add_products(self, products_list, user_id):
        for product in products_list:
            print(product)
            sql = "INSERT INTO Transaction (description, type, amount, currency, user_id) VALUES (%s,%s, %s, %s, %s)"
            val = (str(product.name), str(product.category), float(product.quantity), str(product.cost), user_id)
            sql = "INSERT INTO Transaction (name, category, amount, currency, user_id, created_at, updated_at) VALUES (%s,%s, %s, %s, %s, %s,%s)"
            val = (str(product.name), str(product.category), str(product.price), str(product.currency), user_id,
                   datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
                   datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
            self.cur.execute(sql, val)

        return "OK"

    def add_news(self, company_name, link, description, created_at):
        sql = "INSERT INTO LatestNews (company_name, link, description, created_at, send_in_telegram) VALUES (%s, %s, %s,  %s, %s)"
        val = (company_name, link, description, created_at, "false")
        self.cur.execute(sql, val)
        return "OK"
    def search_for_news(self):
        sql = "SELECT * FROM LatestNews WHERE send_in_telegram = false;"
        self.cur.execute(sql)
        news = self.cur.fetchall()
        return news
    def get_link_news(self):
        sql = "SELECT link FROM LatestNews;"
        self.cur.execute(sql)
        links = self.cur.fetchall()
        return links
    def update_news(self, list_to_update):
        for elm in list_to_update:
            sql = f"UPDATE LatestNews SET send_in_telegram=true WHERE id={int(elm)};"
            self.cur.execute(sql)
    def update_news_true(self):

        sql = f"UPDATE LatestNews SET send_in_telegram=false WHERE id={int(34)};"
        self.cur.execute(sql)
    def commit(self):
        self.conn.commit()
