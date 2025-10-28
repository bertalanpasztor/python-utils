from dataclasses import dataclass


@dataclass
class Database:
    database_name: str
    host: str
    port: int
    user: str
    password: str


@dataclass()
class Table:
    schema_name: str
    table_name: str
