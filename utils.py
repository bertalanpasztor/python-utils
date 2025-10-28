from classes import Database, Table


def read_sheet_to_database_table(sheet_link, database: Database, table: Table) -> None:
    """
    Beolvassa a Google Sheet táblázatot, és betölti a megadott PostgreSQL adatbázis táblájába.
    :param sheet_link: A Google Sheet táblázat linkje
    :param database: A Database osztály példánya az adatbázis kapcsolathoz
    :param table: A Table osztály példánya a cél táblához
    :return: None
    """
    import pandas as pd
    import sqlalchemy

    # Read the Google Sheet into a DataFrame
    sheet_id = sheet_link.split('/d/')[1].split('/')[0]
    gid = sheet_link.split('gid=')[1].split('#')[0]
    csv_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}'
    df = pd.read_csv(csv_url)

    # Database connection parameters
    db_user = database.user
    db_password = database.password
    db_host = database.host
    db_port = database.port
    db_name = database.database_name

    # Create a SQLAlchemy engine
    engine = sqlalchemy.create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

    # create the table first if not exists
    with engine.connect() as connection:
        create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {table.schema_name}.{table.table_name} (
            {" ,".join([f'"{col}" TEXT' for col in df.columns])}
        );
        '''
        connection.execute(sqlalchemy.text(create_table_query))

    # Load DataFrame into PostgreSQL table
    table_name = table.table_name  # Change to your desired table name
    df.to_sql(table_name, engine, if_exists='replace', index=False, schema=table.schema_name)
    print(f"Data loaded into table '{table_name}' successfully.")
