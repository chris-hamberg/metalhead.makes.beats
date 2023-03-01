import os, psycopg2, urllib.parse
from datetime import datetime
try:
    from model.conf import *
except ModuleNotFoundError as production:
    from model.config import *


ADMIN = {"database": DATABASE,
         "user"    : USER,
         "password": PASSWORD,
         "host"    : HOST,
         "port"    : DB_PORT}


def create_tables():
    tables = "model/tables.sql"
    with open(tables, 'r') as fhand:
        sql = fhand.read()
    with psycopg2.connect(**ADMIN) as connection:
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        

class MailingList:


    def create(self, data):
        sql = """INSERT INTO mailing_list (first_name, last_name, email)
                 VALUES (%s, %s, %s);"""
        with psycopg2.connect(**ADMIN) as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(sql, data)
                connection.commit()
            except psycopg2.IntegrityError:
                return False
            else:
                return True
            finally:
                cursor.close()



class FreeBeat:


    def read(self):
        sql  = "SELECT * FROM free_beat;"
        with psycopg2.connect(**ADMIN) as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(sql)
                beats = cursor.fetchall()
            except (psycopg2.OperationalError, IndexError):
                pass
            else:
                return beats
            finally:
                cursor.close()


class Analytics:


    def create(self, data):
        if isinstance(data, dict):
            data = (data.get("ip"), data.get("platform"), data.get("browser"), 
                    data.get("city"), data.get("country"), 
                    data.get("continent"), data.get("bot"), data.get("visits"))
        try:
            data = self.read(data)[0]
            self.update(data)
        except IndexError:
            sql = """INSERT INTO analytics 
                     (ip, platform, browser, city, country, continent, bot, visits)
                     VALUES
                     (%s, %s, %s, %s, %s, %s, %s, %s);"""
            if len(data) == 7:
                data = data + (1,)
            with psycopg2.connect(**ADMIN) as connection:
                cursor = connection.cursor()
                try:
                    cursor.execute(sql, data)
                    connection.commit()
                except psycopg2.IntegrityError:
                    return False
                finally:
                    cursor.close()
        finally:
            data = self.read(data)[0]
            json = {
                "ip"        : data[0],
                "platform"  : data[1],
                "browser"   : data[2],
                "city"      : data[3],
                "country"   : data[4],
                "continent" : data[5],
                "bot"       : data[6],
                "visits"    : data[7],
                "created"   : data[8],
                "last_visit": data[9]}
            return json
            

    def read(self, data = None):
        sql = "SELECT * FROM analytics"
        if data:
            ip = (data[0],)
            sql += " WHERE ip = %s"
        sql += ";"
        with psycopg2.connect(**ADMIN) as connection:
            cursor = connection.cursor()
            try:
                if data:
                    cursor.execute(sql, ip)
                else:
                    cursor.execute(sql)
                data = cursor.fetchall()
            except psycopg2.OperationalError:
                pass
            else:
                return data
            finally:
                cursor.close()


    def update(self, data):
        data   = (data[7] + 1, data[0])
        sql    = """UPDATE analytics SET 
                    visits = %s, last_visit = CURRENT_TIMESTAMP 
                    WHERE ip = %s;"""
        with psycopg2.connect(**ADMIN) as connection:
            cursor = connection.cursor()
            cursor.execute(sql, data)
            connection.commit()
            cursor.close()


class Article:


    def create(self, article):
        sql = """
INSERT INTO article (title, author, descript, article)
VALUES (%s,%s,%s,%s);"""

        with psycopg2.connect(**ADMIN) as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(sql, article)
                connection.commit()
            except psycopg2.IntegrityError:
                return False
            else:
                data = self.read(article[3])[0]
                json = {
                    "id"      : data[0], 
                    "title"   : data[1],
                    "author"  : data[2],
                    "date"    : data[3],
                    "desc"    : data[4],
                    "article" : data[5][:25] + "... "
                    }
                return json
            finally:
                cursor.close()


    def read(self, article=None, id=None):

        assert isinstance(article, str) or (article is None)
        assert isinstance(id, int) or (id is None)

        sql, articles = "SELECT * FROM article", None

        if article:
            sql += f" WHERE article = '{article}'"
        elif id:
            sql += f" WHERE id = '{id}'"
        sql += ";"

        with psycopg2.connect(**ADMIN) as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(sql)
                articles = cursor.fetchall()
            except psycopg2.OperationalError:
                pass
            else:
                return articles
            finally:
                cursor.close()


    def update(self, article):

        data = (article.get("title"), article.get("author"), 
                article.get("desc"), article.get("article"))

        sql = f"""
UPDATE article SET title = %s, author = %s, descript = %s, article = %s
WHERE id = {article.get("id")};"""

        with psycopg2.connect(**ADMIN) as connection:
            cursor = connection.cursor()
            cursor.execute(sql, data)
            connection.commit()
            cursor.close()


    def delete(self, id):

        sql = f"DELETE FROM article WHERE id = {id};"

        with psycopg2.connect(**ADMIN) as connection:
            cursor = connection.cursor()
            cursor.execute(sql)
            connection.commit()
            cursor.close()
