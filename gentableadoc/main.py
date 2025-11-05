"""A program előállítja tables_attributes.adoc fájlt az adatbázisból
amit aztán betudunk illeszteni az Antora dokumentációba
"""

import click
from gentableadoc.Database import Database
from gentableadoc.StructureGenerator import Structure_generator
from gentableadoc.Table import Table
from gentableadoc.database_interface import DatabaseInterface


@click.command()

#@click.option('--database_name', '-d', help='Database name', default='emap_backend')
#@click.option('--database_schema', '-s', help='Database schema', default='emap_backend')
#@click.option('--port', '-p', help='port number', default=5432)
#@click.option('--postgres_user', '-u', help='postgres user', default='postgres')
#@click.option('--postgres_password', '-w', help='postgres password', default='postgres')

@click.option('--database_name', '-d', help='Database name', default='emap_backend')
@click.option('--database_schema', '-s', help='Database schema', default='emap_registry')
@click.option('--port', '-p', help='port number', default=5432)
@click.option('--postgres_user', '-u', help='postgres user', default='postgres')
@click.option('--postgres_password', '-w', help='postgres password', default='postgres')
@click.option('--for_word', '-f', is_flag=True, help='Format for MS Word', default=True)

def main(database_name, port, postgres_user, postgres_password, database_schema, for_word):
    """
    A program fő belépési pontja.
    A paramétereket a parancssorból kapja a program
    :param database_name: adatbázis neve
    :param port: port szám
    :param output_file: kimeneti fájl neve
    :return
    """
    output_file = f'{database_name}__{database_schema}_attributes.adoc'
    db: DatabaseInterface = Database(database_name, host='localhost', port=port, user=postgres_user, password=postgres_password)
    generator = Structure_generator(Table.get_tables(db, database_schema), for_word)
    write_table_structures(generator.get_table_structures(), output_file, database_schema, database_name)
    print(f"Adatbázis struktúra kiírva a '{output_file}' fájlba.")


def write_table_structures(table_structures, output_file, database_schema, database_name):
    """
    A táblák struktúráját kiírja egy fájlba.
    :param table_structures: a táblák struktúrája az asciidoctor számára könnyen feldolgozható formában
    :param output_file: kimeneti fájl neve
    :param database_schema: adatbázis séma neve
    :param database_name: adatbázis neve
    :return: None
    """
    with open(output_file, 'w', encoding='utf8') as f:
        f.write(f""":table-stripes: even
= {database_schema} séma

image::{database_name}__{database_schema}.png[{database_schema} séma kapcsolati diagram, link="./_images/{database_name}__{database_schema}.png",window="_blank"]


""")
        f.write(table_structures)


if __name__ == '__main__':
    main()