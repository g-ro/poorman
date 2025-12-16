import json
from typing import Optional
from models.request_model import RequestModel
from utils.logging_config import logger

class StorageService:
    @staticmethod
    def save_request(request: RequestModel, file_path: str) -> None:
        """Save request configuration to a file"""
        try:
            with open(file_path, 'w') as f:
                json.dump(request.to_dict(), f, indent=2)
        except Exception as e:
            logger.exception("Failed to save request to %s", file_path)
            raise IOError(f"Failed to save request: {str(e)}")
    
    @staticmethod
    def load_request(file_path: str) -> RequestModel:
        """Load request configuration from a file"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            return RequestModel.from_dict(data)
        except Exception as e:
            logger.exception("Failed to load request from %s", file_path)
            raise IOError(f"Failed to load request: {str(e)}")