import json
import os
from typing import Dict, Optional
from dotenv import load_dotenv
from snowflake.snowpark import Session
from snowflake.core import Root
from snowflake.snowpark.exceptions import SnowparkSQLException
import logging

class SnowflakeConnector:
    """A utility class to manage Snowflake connections with proper error handling"""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the Snowflake connector with either provided config or environment variables
        
        Args:
            config (Dict, optional): Connection parameters dictionary. If None, will use environment variables.
        """
        self.logger = logging.getLogger(__name__)
        self.session = None
        self.config = config or self._get_config_from_env()
        
         
        
    def _get_config_from_env(self) -> Dict:
        """Retrieve configuration from environment variables"""
        try:
            return {
                "account": os.environ["SNOWFLAKE_ACCOUNT"],
                "user": os.environ["SNOWFLAKE_USER"],
                "password": os.environ["SNOWFLAKE_PASSWORD"],
                "role": os.environ.get("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
                "database": os.environ.get("SNOWFLAKE_DATABASE"),
                "warehouse": os.environ.get("SNOWFLAKE_WAREHOUSE"),
                "schema": os.environ.get("SNOWFLAKE_SCHEMA")
            }
        except KeyError as e:
            raise ValueError(f"Required environment variable {str(e)} not set")

    def connect(self) -> Session:
        """
        Establish connection to Snowflake
        
        Returns:
            Session: Snowflake session object
            
        Raises:
            SnowparkSQLException: If connection fails
        """
        try:
            self.session = Session.builder.configs(self.config).create()
            self.root = Root(self.session)
            self.logger.info("Successfully connected to Snowflake")
            return self.session
        except SnowparkSQLException as e:
            self.logger.error(f"Failed to connect to Snowflake: {str(e)}")
            raise

    def close(self) -> None:
        """Safely close the Snowflake connection"""
        if self.session:
            try:
                self.session.close()
                self.logger.info("Snowflake connection closed successfully")
            except Exception as e:
                self.logger.error(f"Error closing Snowflake connection: {str(e)}")
        
    def __enter__(self) -> Session:
        """Context manager entry"""
        return self.connect()
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit"""
        self.close()

    def call_model_sql_chat(self,model:str, prompt:str, question:str, temperature:float):
        command = f"""SELECT SNOWFLAKE.CORTEX.COMPLETE(
        '{model}',
        [
            {{
                'role': 'system',
                'content': '{prompt.replace("'", "''")}'
            }},
            {{
                'role': 'user',
                'content': '{question.replace("'", "''")}'
            }}
        ], {{
            'temperature': {temperature}
        }}
        )""".strip()
        res = self.session.sql(command).collect()
        answer = json.loads(res[0][0])["choices"][0]["messages"]
        return str(answer)

    def comple(self,model,prompt):
        res = self.session.sql(f"""SELECT SNOWFLAKE.CORTEX.COMPLETE(
        '{model}',
        '{prompt}'
        )""").collect()
        
        return res

# Example usage:
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        connector = SnowflakeConnector()
        connector.connect()
        result = connector.session.sql("SELECT current_version()").collect()
        print(result)
    except Exception as e:
        print(f"Error: {str(e)}")