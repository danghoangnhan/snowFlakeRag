import logging
from dotenv import load_dotenv
from connector import SnowflakeConnector
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StageManager:
    def __init__(self, connector: 'SnowflakeConnector', stage_name: str = "docs"):
        self.connector = connector
        self.stage_name = stage_name
        self.logger = logging.getLogger(__name__)

    def create_stage(self) -> bool:
        try:
            self.connector.connect()
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
        finally:
            self.connector.close()

    def upload_file(self, file_path) -> bool:
        try:
            self.connector.connect()
            self.connector.session.sql(f"""
                PUT file://{file_path} @{self.stage_name}
                AUTO_COMPRESS = FALSE
                OVERWRITE = TRUE
                """).collect()
            return True
        except Exception as e:
            self.logger.error(f"Upload failed: {str(e)}")
            return False
        finally:
            self.connector.close()

    def list_files(self) -> list:
        try:
            self.connector.connect()
            return self.connector.session.sql(f"LIST @{self.stage_name}").collect()
        except Exception as e:
            self.logger.error(f"Listing files failed: {str(e)}")
            return []
        finally:
            self.connector.close()

    def stage_exists(self) -> bool:
        """
        Check if the stage exists in Snowflake.
        Returns True if the stage exists, False otherwise.
        """
        try:
            self.connector.connect()
            result = self.connector.session.sql(f"""
                SELECT COUNT(*) as count 
                FROM INFORMATION_SCHEMA.STAGES 
                WHERE STAGE_NAME = '{self.stage_name}'
            """).collect()
            
            return result[0]['COUNT'] > 0
        except Exception as e:
            self.logger.error(f"Stage existence check failed: {str(e)}")
            return False
        finally:
            self.connector.close()

    def remove_file(self, file_name: str) -> bool:
        """
        Remove a specific file from the Snowflake stage.
        Args:
            file_name: Name of the file to remove from the stage
        Returns:
            bool: True if removal successful, False otherwise
        """
        try:
            self.connector.connect()
            self.connector.session.sql(f"""
                REMOVE @{self.stage_name}/{file_name}
            """).collect()
            return True
        except Exception as e:
            self.logger.error(f"File removal failed: {str(e)}")
            return False
        finally:
            self.connector.close()

    def remove_all_files(self) -> bool:
        """
        Remove all files from the Snowflake stage.
        Returns:
            bool: True if removal successful, False otherwise
        """
        try:
            self.connector.connect()
            self.connector.session.sql(f"""
                REMOVE @{self.stage_name}
            """).collect()
            return True
        except Exception as e:
            self.logger.error(f"Removing all files failed: {str(e)}")
            return False
        finally:
            self.connector.close()


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