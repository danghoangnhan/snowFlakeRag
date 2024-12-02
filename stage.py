import logging
import os
import tempfile

from connector import SnowflakeConnector


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

    def upload_file(self, file) -> bool:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(file.getvalue())
            tmp_file_path = tmp_file.name
        
        try:
            self.connector.connect()
            self.connector.session.sql(f"""
                PUT file://{tmp_file_path} @{self.stage_name}
                AUTO_COMPRESS = FALSE
                OVERWRITE = TRUE
            """).collect()
            return True
        except Exception as e:
            self.logger.error(f"Upload failed: {str(e)}")
            return False
        finally:
            os.unlink(tmp_file_path)
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