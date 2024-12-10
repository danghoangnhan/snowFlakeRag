
    
# src/stage/dao.py
from typing import List, Optional
import logging
from src.base.dao import BaseDAO
from src.stage.model import StageFile

class SnowflakeStageDAO(BaseDAO):
    def __init__(self):
        super().__init__()
        self.stage_name = "docs"
        self.logger = logging.getLogger(__name__)

    def get_stage_files(self,dir) -> List[StageFile]:
        """Get list of all files in stage"""
        try:
            query = f"LIST @{self.stage_name}/{dir}"
            result = self.execute_query(query)
            
            files = []
            for row in result:
                row_dict = {k.lower(): v for k, v in row.asDict().items()}
                files.append(StageFile(**row_dict))
            return files
        except Exception as e:
            self.logger.error(f"Failed to list stage files: {str(e)}")
            return []

    def get_file_url(self, file_path: str, expiration: int = 3600) -> Optional[str]:
        """Get presigned URL for file access"""
        try:
            query = f"""
            SELECT GET_PRESIGNED_URL(
                @{self.stage_name}, 
                '{file_path}',
                {expiration}
            ) as url
            """
            result = self.execute_query(query)
            return result[0]['URL'] if result else None
        except Exception as e:
            self.logger.error(f"Failed to get file URL: {str(e)}")
            return None

    def upload_file(self, file_path: str,session_id:str) -> bool:
        """Upload file to stage"""
        try:
            file_path = file_path.replace('\\', '/').replace("'", "''")
            
            # file_path = f"'{file_path}'"
            query = f"""
            PUT 'file://{file_path}' @{self.stage_name}/{session_id}
            AUTO_COMPRESS = FALSE
            OVERWRITE = TRUE
            """
            self.execute_query(query)
            return True
        except Exception as e:
            self.logger.error(f"Failed to upload file: {str(e)}")
            return False

        
    def remove_file(self,dir_name:str, file_name: str) -> bool:
        """
        Remove a specific file from the Snowflake stage.
        Args:
            file_name: Name of the file to remove from the stage
        Returns:
            bool: True if removal successful, False otherwise
        """
        try:
            self.connector.session.sql(f"""
                REMOVE @{self.stage_name}/{dir_name}{file_name}
            """).collect()
            return True
        except Exception as e:
            self.logger.error(f"File removal failed: {str(e)}")
            return False

    def remove_dir(self,dir_name:str) -> bool:
        """
        Remove all files from the Snowflake stage.
        Returns:
            bool: True if removal successful, False otherwise
        """
        try:
            self.connector.session.sql(f"""
                REMOVE @{self.stage_name}/{dir_name}
            """).collect()
            return True
        except Exception as e:
            self.logger.error(f"Removing all files failed: {str(e)}")
            return False
