import datetime

import pymysql.cursors
class DBmanager:
    def __init__(self):

        self.conn = pymysql.connect(host="188.244.45.227",
                       port = 3306,
                       user="sigma",
                       password="j$sdjk!53",
                       db="main_db",
                       charset='utf8',
                       )
        self.cur = self.conn.cursor()

    def add_products(self, products_list, user_id):
        for product in products_list:
            print(product)
            sql = "INSERT INTO Transaction (name, category, amount, currency, user_id, created_at, updated_at) VALUES (%s,%s, %s, %s, %s, %s,%s)"
            val = (str(product.name), str(product.category), str(product.price), str(product.currency), user_id, datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") )
            self.cur.execute(sql,val)

        return "OK"
    def commit(self):
        self.conn.commit()
