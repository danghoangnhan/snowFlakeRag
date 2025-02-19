import logging
from dotenv import load_dotenv
from src.base.connector import SnowflakeConnector, get_resource_manager
logging.basicConfig(level=logging.INFO)

class StageManager:
    def __init__(self, stage_name: str = "docs"):
        self.connector = get_resource_manager()
        self.stage_name = stage_name
        self.logger = logging.getLogger(__name__)

    def create_stage(self) -> bool:
        try:
            self.connector.session.sql(f"""
                CREATE OR REPLACE STAGE {self.stage_name}
                ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
                DIRECTORY = (
                    ENABLE = true,
                    REFRESH_ON_CREATE = true,
                    AUTO_REFRESH = true
                )
                COMMENT = 'Secure stage for storing and processing PDF documents'
            """).collect()
            return True
        except Exception as e:
            self.logger.error(f"Stage creation failed: {str(e)}")
            return False

    def upload_file(self, file_path:str,session_id:str) -> bool:
        try:
            self.connector.session.sql(f"""
    def upload_file(self, file_path:str,session_id:str) -> bool:
                PUT file://{file_path} @{self.stage_name}/{session_id}
                AUTO_COMPRESS = FALSE
                OVERWRITE = TRUE
                """).collect()
            return True
        except Exception as e:
            self.logger.error(f"Upload failed: {str(e)}")
            return False

    def list_files(self,dir) -> list:
        try:
            return self.connector.session.sql(f"LIST @{self.stage_name}/{dir}").collect()
        except Exception as e:
            self.logger.error(f"Listing files failed: {str(e)}")
            return []
        
    def stage_exists(self) -> bool:
        """
        Check if the stage exists in Snowflake.
        Returns True if the stage exists, False otherwise.
        """
        try:
            result = self.connector.session.sql(f"""
                SELECT COUNT(*) as count 
                FROM INFORMATION_SCHEMA.STAGES 
                WHERE STAGE_NAME = '{self.stage_name}'
            """).collect()
            
            return result[0]['COUNT'] > 0
        except Exception as e:
            self.logger.error(f"Stage existence check failed: {str(e)}")
            return False