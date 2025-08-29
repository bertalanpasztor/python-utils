"""
Ez a modul tartalmazza a Database osztályt, amely a kapcsolatot valósítja meg az adatbázissal.
Ezenkívül a Database osztály tartalmazza a táblák lekérdezését is.
"""

import psycopg2
from gentableadoc.database_interface import DatabaseInterface


class Database(DatabaseInterface):
    def __init__(self, name: str, port=5432, host='localhost', user='postgres',  password='postgres'):
        """
        Konstruktor
        :param name: adatbázis neve
        :param port: port szám
        :param host: host neve
        :param password: jelszó
        """
        self.name = name
        self.host = host
        self.port = port
        self.user = user
        passw = password
        self.__connection_string = f"postgres://{self.user}:{passw}@{host}:{port}/{name}"
        self.conn = psycopg2.connect(self.__connection_string)


    def execute_query(self, cmd):
        """
        A kapott SQL parancsot végrehajtja és visszaadja az eredményt
        :param cmd: SQL parancs
        :return: eredmény
        """
        conn = self.conn
        cur = conn.cursor()
        cur.execute(cmd)
        records = cur.fetchall()
        conn.commit()
        cur.close()
        return records