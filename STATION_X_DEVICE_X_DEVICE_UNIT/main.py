""" A program beolvassa egy Google Sheet táblázat adatait, és betölti egy PostgreSQL adatbázis táblájába. """
from classes import Database, Table
from utils import read_sheet_to_database_table

if __name__ == '__main__':
    sheet_link = "https://docs.google.com/spreadsheets/d/1w-ZFpe2YZ-mTE_lOkUjt-u4C-ED8mqeq/edit?gid=716677592#gid=716677592"
    database = Database(
        database_name='akp_be',
        host='localhost',
        port=5432,
        user ='postgres',
        password='postgres'
    )
    table = Table(
        schema_name='public',
        table_name='teszt1'
    )
    read_sheet_to_database_table(sheet_link, database, table)