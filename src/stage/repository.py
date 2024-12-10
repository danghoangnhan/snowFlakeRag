# src/stage/repository.py
import logging
from typing import List, Dict, Optional
import os
from src.stage.dao import SnowflakeStageDAO
from src.stage.model import StageFile

class StageRepository:
    def __init__(self):
        self.stage_dao = SnowflakeStageDAO()
        self.logger     = logging.getLogger(__name__)
        
    def list_files(self) -> List[StageFile]:
        """Get list of all files in stage"""
        return self.stage_dao.get_stage_files()

    def get_file_info(self, file_path: str) -> Optional[StageFile]:
        """Get information about specific file"""
        files = self.stage_dao.get_stage_files()
        return next((f for f in files if f.name == file_path), None)

    def get_file_url(self, file_path: str, expiration: int = 3600) -> Optional[str]:
        """Get temporary access URL for file"""
        return self.stage_dao.get_file_url(file_path, expiration)

    def upload_files(self, file_paths: List[str]) -> Dict[str, bool]:
        """
        Upload multiple files to stage
        Returns: Dict mapping file paths to success status
        """
        results = {}
        for file_path in file_paths:
            if not os.path.exists(file_path):
                self.logger.warning(f"File not found: {file_path}")
                results[file_path] = False
                continue
                
            success = self.stage_dao.upload_file(file_path)
            results[file_path] = success
        return results

    def remove_files(self, file_paths: List[str]) -> Dict[str, bool]:
        """
        Remove multiple files from stage
        Returns: Dict mapping file paths to success status
        """
        results = {}
        for file_path in file_paths:
            success = self.stage_dao.remove_file(file_path)
            results[file_path] = success
        return results

    def get_stage_stats(self) -> Dict:
        """Get stage statistics"""
        files = self.stage_dao.get_stage_files()
        if not files:
            return {
                'total_files': 0,
                'total_size': 0,
                'avg_file_size': 0
            }

        total_size = sum(f.size for f in files)
        return {
            'total_files': len(files),
            'total_size': total_size,
            'avg_file_size': total_size / len(files)
        }

# Example usage
"""
# Initialize repository
stage_repo = StageRepository()

# List files
files = stage_repo.list_files()
for file in files:
    print(f"File: {file.name}, Size: {file.size}")

# Upload files
results = stage_repo.upload_files(["document1.pdf", "document2.pdf"])
for path, success in results.items():
    print(f"Upload {path}: {'Success' if success else 'Failed'}")

# Get file URL
url = stage_repo.get_file_url("document1.pdf")
if url:
    print(f"Access URL: {url}")

# Get statistics
stats = stage_repo.get_stage_stats()
print(f"Total files: {stats['total_files']}")
print(f"Total size: {stats['total_size']} bytes")
"""