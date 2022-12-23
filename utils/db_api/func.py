from sqlite3 import Error
import sqlite3
from time import ctime
from datetime import datetime
from xlsxwriter.workbook import Workbook
import pytz

class DBS:
    def post_sql_query(sql_query):
        with sqlite3.connect('./my.db') as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(sql_query)
            except Error:
                pass
            result = cursor.fetchall()
            return result


    def create_tables(self):
        users_query = '''CREATE TABLE IF NOT EXISTS USERS
                            (user_id INTEGER PRIMARY KEY NOT NULL,
                            username TEXT,
                            first_name TEXT,
                            last_name TEXT,
                            reg_date TEXT);'''

        self.post_sql_query(users_query)

    def create_tables_(self):
        query = '''CREATE TABLE "Groups" (
                "id"	INTEGER,
                "link"	TEXT,
                "count"	INTEGER,
                "chat_id"	TEXT,
                "name"	TEXT,
                "user_id"	TEXT,
                "start_status"	TEXT,
                "status"	TEXT,
                PRIMARY KEY("id" AUTOINCREMENT)
                );'''
        self.post_sql_query(query)
        
    def register_user(self, user, username, first_name, last_name):
        user_check_query = f'SELECT * FROM USERS WHERE user_id = {user};'
        user_check_data = self.post_sql_query(user_check_query)
        if not user_check_data:
            insert_to_db_query = f'INSERT INTO USERS (user_id, username, first_name,  last_name, reg_date) VALUES ' \
                                f'({user}, "{username}", "{first_name}", "{last_name}", "{ctime()}");'
            self.post_sql_query(insert_to_db_query)

    def register_group(self, link, count, chat_id, name, user_id, start_status):
        user_check_query = f'SELECT * FROM Groups WHERE chat_id = {chat_id};'
        user_check_data = self.post_sql_query(user_check_query)
        if not user_check_data:
            insert_to_db_query = f'INSERT INTO Groups (link, count, chat_id,  name, user_id, start_status) VALUES ' \
                                f'("{link}", "{count}", "{chat_id}", "{name}", "{user_id}", "{start_status}");'
            print(insert_to_db_query)
            self.post_sql_query(insert_to_db_query)

    def update_group(self, link, count, status, chat_id):
        lang_query = f"UPDATE Groups set link='{link}', count={count}, status='{status}'   where chat_id={chat_id} "
        self.post_sql_query(lang_query)

    def group_count(self):
        query = "SELECT COUNT(*) Groups"
        data = self.post_sql_query(query)
        return data[0][0]
    
    def user_count(self):
        query = "SELECT COUNT(*) USERS"
        data = self.post_sql_query(query)
        return data[0][0]

DBS.create_tables(DBS)
