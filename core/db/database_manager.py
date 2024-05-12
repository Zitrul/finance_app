import aiomysql
import bcrypt
import mysql.connector
import aiohttp
import json

from core.settings import *


class DatabaseManager_thread:
    def __init__(self) -> None:
        self.db = None

    def connect(self):
        self.db = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            db=DB,
            autocommit=True
        )
        self.cursor = self.db.cursor()

    def disconnect(self):
        self.cursor.close()
        self.db.close()

    def get_all_users_id(self) -> tuple:
        self.connect()
        self.cursor.execute("SELECT telegram_auth FROM User WHERE telegram_auth is not NULL")
        self.answer = self.cursor.fetchall()
        self.disconnect()
        return [int(row[0]) for row in self.answer]


class DatabaseManager:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await aiomysql.create_pool(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            db=DB,
            autocommit=True
        )

    async def disconnect(self):
        self.pool.close()
        await self.pool.wait_closed()

    async def update_user_token(self, user_id: int, token: str) -> bool:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                query = f"UPDATE User SET telegram_bot_token = '0', telegram_auth = '{user_id}'" \
                        f" WHERE telegram_bot_token = '{token}'"
                await cur.execute(query)
                return cur.rowcount > 0

    async def insert_user_info(self, user_id: int, column: str, args: str) -> None:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                query = f"UPDATE User SET {column} = %s WHERE telegram_auth = '{user_id}'"
                await cur.execute(query, (args,))

    async def check_password(self, user_id: int | str, input_passwd: str) -> bool:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                query = f"SELECT password FROM User WHERE telegram_auth = '{user_id}'"
                await cur.execute(query)
                passwd = await cur.fetchone()
                passwd = passwd[0]
                return bcrypt.checkpw(input_passwd.encode(encoding), passwd.encode(encoding))

    async def get_all_users(self) -> list:
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                query = "SELECT * FROM User"
                await cur.execute(query)
                rows = await cur.fetchall()
                return [dict(row) for row in rows]

    async def get_transactions(self, user_id: str | int) -> list:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                query = f"SELECT id FROM User WHERE telegram_auth = '{user_id}'"
                await cur.execute(query)
                user_id = await cur.fetchone()
                query = f"SELECT id, name, amount, category FROM Transaction WHERE user_id = '{user_id[0]}'"
                await cur.execute(query)
                return await cur.fetchall()

    async def get_user_by_telegram_id(self, telegram_id: int):
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                query = "SELECT * FROM User WHERE telegram_auth = %s"
                await cur.execute(query, (telegram_id,))
                user = await cur.fetchone()
                return dict(user) if user else None

    async def get_all_share(self, user_id):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                user_id = await self.get_user_by_telegram_id(user_id)
                user_id = user_id['id']
                query = 'SELECT id, stock_quote, asset_amount, asset_buy_price, company_name FROM UserAssets WHERE user_id = %s'
                await cur.execute(query, (user_id, ))
                res = await cur.fetchall()
                return [i for i in res]

    async def change_transaction(self, trn_id, name, amount, category):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                query = "UPDATE Transaction SET name = %s, amount = %s, category = %s WHERE id = %s"
                await cur.execute(query, (name, amount, category, trn_id))

    async def change_deposit(self, dep_id, name, amount, telegram_id):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                query = f"SELECT id FROM User WHERE telegram_auth = '{telegram_id}'"
                await cur.execute(query)
                user_id = await cur.fetchone()
                query = "UPDATE ProfitableTransaction SET name = %s, amount = %s WHERE id = %s and user_id = %s"
                await cur.execute(query, (name, amount, dep_id, user_id))
                    
    async def delete_share_by_id(self, id, telegram_id):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                query = f"SELECT id FROM User WHERE telegram_auth = '{telegram_id}'"
                await cur.execute(query)
                user_id = await cur.fetchone()
                query = 'DELETE FROM UserAssets WHERE id = %s and user_id = %s'
                await cur.execute(query, (id, user_id))
    
    async def get_all_amount_salary(self, telegram_id : int) -> int:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    query = f"SELECT id FROM User WHERE telegram_auth = '{telegram_id}'"
                    await cur.execute(query)
                    user_id = await cur.fetchone()
                    query = f"SELECT amount FROM ProfitableTransaction WHERE user_id = '{user_id[0]}'"
                    await cur.execute(query)
                    return sum([int(elem[0]) for elem in await cur.fetchall()])
                
    async def get_all_salary(self, telegram_id):
        async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    user_id = await self.get_user_by_telegram_id(telegram_id)
                    query = f"SELECT id, name, amount, category, currency FROM ProfitableTransaction WHERE user_id = '{user_id['id']}'"
                    await cur.execute(query)
                    return await cur.fetchall()

    async def get_all_amount_share(self, telegram_id : int) -> int:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                query = f"SELECT id FROM User WHERE telegram_auth = '{telegram_id}'"
                await cur.execute(query)
                user_id = await cur.fetchone()
                query = f"SELECT stock_quote, asset_amount FROM UserAssets WHERE user_id = '{user_id[0]}'"
                await cur.execute(query)
                api = f'http://{HOST}:{PORT_API}/get_current_price?ticker='
                price_share = []
                for elem in await cur.fetchall():
                    async with aiohttp.ClientSession() as session:
                        async with session.get(api + elem[0]) as resp:

                            price_share.append(int(json.loads(await resp.text())["price"]) * int(elem[1]))
                return sum(price_share)


    async def get_all_transaction_amount(self, telegram_id: int) -> list:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                query = f"SELECT id FROM User WHERE telegram_auth = '{telegram_id}'"
                await cur.execute(query)
                user_id = await cur.fetchone()
                query = f"SELECT amount FROM Transaction WHERE user_id = '{user_id[0]}'"
                await cur.execute(query)
                return [int(elem[0]) for elem in await cur.fetchall()]
            
            
    async def is_user_by_telegram_id(self, telegram_id: int) -> bool:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                query = "SELECT EXISTS(SELECT 1 FROM User WHERE telegram_auth = %s) AS 'exists'"
                await cur.execute(query, (telegram_id,))
                result = await cur.fetchone()
                return result[0] == 1

    async def get_token_by_login_password(self, email_auth: str, password: str):
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                query = "SELECT telegram_bot_token, password FROM User WHERE email_auth = %s"
                await cur.execute(query, (email_auth,))
                user = await cur.fetchone()

                if user:
                    password_bytes = password.encode('utf-8')
                    hashed_password = user['password'].encode('utf-8')

                    if bcrypt.checkpw(password_bytes, hashed_password):
                        return user['telegram_bot_token']

                return None
