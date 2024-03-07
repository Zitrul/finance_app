import pymysql.cursors


class DBmanager:
    def init(self):

        self.conn = pymysql.connect(host="188.244.45.227",
                                    port=3306,
                                    user="sigma",
                                    password="j$sdjk!53",
                                    db="main_db",
                                    charset='utf8',
                                    )
        self.cur = self.conn.cursor()

    def add_products(self, products_list, user_id):
        for product_name in products_list:
            product = products_list[product_name]
            print(product)
            sql = "INSERT INTO Transaction (description, type, amount, currency, sum, user_id) VALUES (%s,%s, %s,%s, %s, %s)"
            val = (
            product_name, product["category"], float(product["quantity"]), str(product["price"]), str(product["cost"]),
            user_id)
            self.cur.execute(sql, val)

        return "OK"

    def add_news(self, company_name, link, description, created_at):
        sql = "INSERT INTO LatestNews (company_name, link, description, created_at) VALUES (%s, %s, %s,  %s)"
        val = (company_name, link, description, created_at)
        self.cur.execute(sql, val)
        return "OK"

    def commit(self):
        self.conn.commit()
