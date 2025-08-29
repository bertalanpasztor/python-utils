"""
Table osztály
Ez az osztály egy adatbázis táblát reprezentál.
Ezenkívül a táblával kapcsolatos metódusokat.
"""
from dataclasses import dataclass

import psycopg2


@dataclass
class Table:
    conn: psycopg2.extensions.connection
    schema: str
    name: str

    @staticmethod
    def get_tables(db, schema) -> dict[str, list]:
        """
        Visszaad egy szótárat Table objektumokkal, formátum: {table_name: schema.tablename}
        """
        rows = db.execute_query(f"""
            SELECT schemaname, relname
            FROM pg_catalog.pg_stat_all_tables 
            WHERE schemaname = '{schema}'
              AND relname not like '%\_p2%' AND schemaname not like 'pg\_%'
              AND relname not like '%\_default'
              AND relname not like '%$hist%'
            ORDER BY schemaname, relname """)

        tables = [Table(db.conn, *row) for row in rows]
        return tables

    def get_structure(self):
        """
        Visszaadja a tábla struktúráját egy listában.
        :return: a tábla oszlopainak leíró rekordjai
        """
        cur = self.conn.cursor()
        cur.execute(f"""SELECT
		column_name,
    CASE
        WHEN data_type = 'character varying' THEN 'VARCHAR(' || character_maximum_length || ')'
        WHEN data_type = 'character' THEN 'CHAR(' || character_maximum_length || ')'
        WHEN data_type = 'numeric' THEN 'NUMERIC(' || numeric_precision || ', ' || numeric_scale || ')'
        WHEN data_type = 'timestamp without time zone' THEN 'TIMESTAMP'
        WHEN data_type = 'timestamp without time zone' THEN 'TIMESTAMP'
        ELSE UPPER(data_type)
    END AS column_type,
    column_default,
    CASE
        WHEN is_nullable = 'YES' THEN 'igen'
        ELSE 'nem'
    END AS is_nullable,
    col_description(format('%s.%s', table_schema, table_name)::regclass::oid, ordinal_position) AS comment
FROM
    information_schema.columns
WHERE
    table_schema = '{self.schema}'
    AND table_name = '{self.name}'
""")
        out = cur.fetchall()
        return out

