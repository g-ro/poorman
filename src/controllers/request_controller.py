from typing import Optional, Callable
import threading
from tkinter import messagebox

from models.request_model import RequestModel
from models.response_model import ResponseModel
from services.request_service import RequestService
from services.storage_service import StorageService

class RequestController:
    def __init__(self, on_response_received: Callable[[ResponseModel], None]):
        self.request_service = RequestService()
        self.storage_service = StorageService()
        self.on_response_received = on_response_received
        self.current_request: Optional[RequestModel] = None
    
    def send_request(self, request: RequestModel):
        """Send HTTP request in a separate thread"""
        self.current_request = request
        threading.Thread(target=self._send_request_thread, daemon=True).start()
    
    def _send_request_thread(self):
        """Handle request sending in a separate thread"""
        try:
            response = self.request_service.send_request(self.current_request)
            # Notify UI with response
            self.on_response_received(response)
        except Exception as e:
            messagebox.showerror("Request Error", str(e))
    
    def save_request(self, request: RequestModel, file_path: str):
        """Save request configuration to file"""
        try:
            self.storage_service.save_request(request, file_path)
        except Exception as e:
            messagebox.showerror("Save Error", str(e))
    
    def load_request(self, file_path: str) -> Optional[RequestModel]:
        """Load request configuration from file"""
        try:
            return self.storage_service.load_request(file_path)
        except Exception as e:
            messagebox.showerror("Load Error", str(e))
            return None
    
    def setup_oauth2(self, client_id: str, redirect_uri: str, scope: str = None) -> Optional[str]:
        """Set up OAuth2 authentication"""
        try:
            return self.request_service.setup_oauth2_session(client_id, redirect_uri, scope)
        except Exception as e:
            messagebox.showerror("OAuth2 Error", str(e))
            return None
    
    def get_oauth2_token(self, code: str, client_secret: str, token_url: str) -> bool:
        """Get OAuth2 token using authorization code"""
        try:
            self.request_service.get_oauth2_token(code, client_secret, token_url)
            return True
        except Exception as e:
            messagebox.showerror("OAuth2 Error", str(e))
            return False 