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
if __name__ == "__main__":

    load_dotenv('envs/dev.env')  # Load environment variables from .env file

    connector = SnowflakeConnector()
    connector.connect()
    stage_manager = StageManager(connector, "docs")
    
    test_file = "test.pdf"
    
    try:
        # # # 1. First check if stage exists
        # # logger.info("Checking if stage exists...")
        # # if not stage_manager.stage_exists():
        # #     logger.info("Stage doesn't exist, creating new stage...")
        # #     stage_manager.create_stage()
        
        # 2. Upload file
        logger.info("Uploading test file...")
        if stage_manager.upload_file(test_file):
            logger.info("File uploaded successfully")
        else:
            logger.error("File upload failed")
        
        # 3. List files
        # logger.info("Listing files in stage...")
        # files = stage_manager.list_files()
        # if files:
        #     logger.info("Files in stage:")
        #     for file in files:
        #         logger.info(f"- {file}")
        # else:
        #     logger.info("No files found in stage")
        
        # # 4. Remove the file
        # logger.info("Removing test file...")
        # uploaded_filename = files[0]['name'] if files else "test_file"  # Get the actual filename
        # if stage_manager.remove_file(uploaded_filename):
        #     logger.info("File removed successfully")
        # else:
        #     logger.error("File removal failed")
        
        # # 5. Verify removal by listing files again
        # logger.info("Verifying removal - listing files again...")
        # remaining_files = stage_manager.list_files()
        # if not remaining_files:
        #     logger.info("Stage is empty - file was successfully removed")
        # else:
        #     logger.warning("Files still remain in stage:")
        #     for file in remaining_files:
        #         logger.info(f"- {file}")
                
    except Exception as e:
        logger.error(f"Test failed with error: {str(e)}")