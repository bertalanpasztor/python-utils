# gentableadoc/database_interface.py
from abc import ABC, abstractmethod

class DatabaseInterface(ABC):

    @abstractmethod
    def execute_query(self, query: str):
        pass