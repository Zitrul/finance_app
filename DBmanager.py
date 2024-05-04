import datetime

import pymysql.cursors


class DBmanager:
    def __init__(self):

        self.conn = pymysql.connect(host="46.188.100.158",
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
            sql = "INSERT INTO Transaction (name, category, amount, currency, user_id, created_at, updated_at) VALUES (%s,%s, %s, %s, %s, %s,%s)"
            val = (str(product.name), str(product.category), str(product.price), str(product.currency), user_id,
                   datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
                   datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
            self.cur.execute(sql, val)

        return "OK"
    def add_p_transactions(self, user_id, amount, t_type, name):

        sql = "INSERT INTO ProfitableTransaction (name, category, amount, currency, user_id, created_at, updated_at) VALUES (%s,%s, %s, %s, %s, %s, %s)"
        val = (str(name), str(t_type), str(amount), str('RUB'), user_id,
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

    def get_users_assets(self, user_id):
        sql = f"SELECT company_name FROM UserAssets WHERE news_subscription = true AND user_id = {user_id};"
        self.cur.execute(sql)
        companies = self.cur.fetchall()
        return companies

    def add_users_asset(self, company_name,news_subscription, user_id, asset_amount,stock_quote, asset_buy_price):
        print(asset_amount, asset_buy_price)
        if news_subscription == "true":
            news_subscription = 1
        elif news_subscription == "True":
            news_subscription = 1
        else:
            news_subscription = 0
        sql = "INSERT INTO UserAssets (company_name,asset_buy_price, news_subscription, user_id, asset_amount, created_at, stock_quote,  updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        self.cur.execute(sql, (company_name,asset_buy_price, news_subscription, user_id, asset_amount, datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), stock_quote, datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))
        companies = self.cur.fetchall()
        return companies
    def get_users_assets(self, user_id):
        sql = f"SELECT company_name, stock_quote, asset_amount, asset_buy_price   FROM UserAssets WHERE user_id = {user_id};"
        self.cur.execute(sql)
        companies = self.cur.fetchall()
        result = {}
        for i in companies:
            if i[1] in result:
                result[i[1]]["price"] += float(i[2]) * float(i[3])
                result[i[1]]["amount"] += float(i[2])
            else:
                result[i[1]] = {}
                result[i[1]]["price"] = float(i[2]) * float(i[3])
                result[i[1]]["amount"] = float(i[2])
        return result
    def modify_users_assets(self, user_id,amount_to_sell, ticker):
        sql = f"SELECT id, asset_amount, asset_buy_price FROM UserAssets WHERE stock_quote = '{ticker}' AND user_id = {user_id};"
        self.cur.execute(sql)
        ticker_amounts = self.cur.fetchall()

        print(ticker_amounts)

        if len(ticker_amounts) == 0:
            return {"error":"No such ticker"}

        dict_how_many = {}
        sold_on_price = 0
        sum = amount_to_sell
        for i in range(len(ticker_amounts)):
            if float(ticker_amounts[i][1]) < sum:
                sold_on_price += float(ticker_amounts[i][1]) * float(ticker_amounts[i][2])
                dict_how_many[float(ticker_amounts[i][0])] = 0
                sum -= float(ticker_amounts[i][1])
            else:

                sold_on_price += (sum) * float(ticker_amounts[i][2])
                dict_how_many[float(ticker_amounts[i][0])] = float(ticker_amounts[i][1])-sum
                sum = 0
                break
        if sum != 0:
            return {"error": "No enough assets available"}

        print(dict_how_many)

        for id in dict_how_many.keys():
            if dict_how_many[id] != 0:
                sql = f"UPDATE UserAssets SET asset_amount = {dict_how_many[id]} WHERE id = {id} AND user_id = {user_id};"
                self.cur.execute(sql)
            else:
                sql = f"DELETE FROM UserAssets WHERE id = {id} AND user_id = {user_id};"
                self.cur.execute(sql)

        return {"success": True,
                "sell_on_price":sold_on_price}
    def get_transactions_by_date(self, user_id, from_date):
        sql = f"SELECT created_at, amount FROM Transaction WHERE user_id = {user_id};"
        self.cur.execute(sql)
        transactions = self.cur.fetchall()

        sql = f"SELECT created_at, amount FROM ProfitableTransaction WHERE user_id = {user_id};"
        self.cur.execute(sql)
        profitable_transactions = self.cur.fetchall()

        start_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')
        end_date = datetime.datetime.now()
        day = start_date + datetime.timedelta(days=1)
        print(transactions)
        print(profitable_transactions)
        result = dict()
        for i in range((end_date - start_date).days):
            day = day + datetime.timedelta(days=1)
            day_string = day.strftime('%Y-%m-%d')
            result[day_string] = 0
            for profit in profitable_transactions:
                if profit[0] <= day:
                    result[day_string] += float(profit[1])
            for transaction in transactions:
                if transaction[0] <= day:
                    result[day_string] -= float(transaction[1])
        return result
    def delete_profit_transaction(self, user_id, transaction_id):
        sql = f"DELETE FROM ProfitableTransaction WHERE id = {transaction_id} AND user_id = {user_id};"
        self.cur.execute(sql)
    def delete_transaction(self, user_id, transaction_id):
        sql = f"DELETE FROM Transaction WHERE id = {transaction_id} AND user_id = {user_id};"
        self.cur.execute(sql)
    def commit(self):
        self.conn.commit()

