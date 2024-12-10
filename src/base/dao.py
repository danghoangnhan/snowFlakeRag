import logging
from sqlite3 import Row
from typing import List, Dict
from abc import ABC
from src.base.connector import  get_resource_manager

class BaseDAO(ABC):
    def __init__(self):
        self.connector = get_resource_manager()
        self.logger = logging.getLogger(__name__)
        
    def execute_query(self, query: str, params: tuple = None) -> List[Row]:
        """Execute a query and return results"""
        try:
            if params:
                result = self.connector.session.sql(query, params=params).collect()
            else:
                result = self.connector.session.sql(query,params=params).collect()
            return result
        except Exception as e:
            print(f"Error executing query: {e}")
            raise