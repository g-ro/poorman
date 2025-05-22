import json
import time
from typing import Optional
import requests
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth1, OAuth2Session
import urllib3

from models.request_model import RequestModel
from models.response_model import ResponseModel

# Disable SSL warnings for testing purposes
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class RequestService:
    def __init__(self):
        self.oauth_session: Optional[OAuth2Session] = None
        self.oauth_token: Optional[dict] = None
    
    def send_request(self, request: RequestModel) -> ResponseModel:
        """Send an HTTP request and return the response"""
        try:
            start_time = time.time()
            
            # Prepare authentication
            auth = self._prepare_auth(request)
            
            # Prepare request data
            data = None
            json_data = None
            
            if request.body_type == "raw":
                data = request.body_content
            elif request.body_type == "json":
                try:
                    json_data = json.loads(request.body_content)
                    request.headers["Content-Type"] = "application/json"
                except json.JSONDecodeError:
                    if request.body_content.strip():
                        raise ValueError("Invalid JSON format")
            elif request.body_type == "form":
                data = request.form_data
            
            # Make request
            response = requests.request(
                method=request.method,
                url=request.url,
                params=request.params,
                headers=request.headers,
                data=data,
                json=json_data,
                auth=auth,
                verify=False,  # For HTTPS with self-signed certificates
                timeout=30
            )
            
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            return ResponseModel(
                status_code=response.status_code,
                reason=response.reason,
                headers=dict(response.headers),
                content=response.content,
                elapsed_time=elapsed_time
            )
            
        except Exception as e:
            return ResponseModel.from_error(e)
    
    def _prepare_auth(self, request: RequestModel):
        """Prepare authentication for the request"""
        auth = None
        
        if request.auth_type == "basic":
            username = request.auth_data.get("username", "")
            password = request.auth_data.get("password", "")
            if username or password:
                auth = HTTPBasicAuth(username, password)
        
        elif request.auth_type == "bearer":
            token = request.auth_data.get("token", "")
            if token:
                request.headers["Authorization"] = f"Bearer {token}"
        
        elif request.auth_type == "oauth1":
            consumer_key = request.auth_data.get("consumer_key", "")
            consumer_secret = request.auth_data.get("consumer_secret", "")
            token = request.auth_data.get("access_token", "")
            token_secret = request.auth_data.get("token_secret", "")
            
            if all([consumer_key, consumer_secret]):
                auth = OAuth1(consumer_key, consumer_secret, token, token_secret)
        
        elif request.auth_type == "oauth2" and self.oauth_token:
            request.headers["Authorization"] = f"Bearer {self.oauth_token.get('access_token', '')}"
        
        return auth
    
    def setup_oauth2_session(self, client_id: str, redirect_uri: str, scope: str = None) -> str:
        """Set up OAuth2 session and return the authorization URL"""
        self.oauth_session = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope.split() if scope else None)
        authorization_url, _ = self.oauth_session.authorization_url(request.auth_data["auth_url"])
        return authorization_url
    
    def get_oauth2_token(self, code: str, client_secret: str, token_url: str) -> dict:
        """Get OAuth2 token using authorization code"""
        if not self.oauth_session:
            raise ValueError("OAuth2 session not initialized")
        
        self.oauth_token = self.oauth_session.fetch_token(
            token_url,
            code=code,
            client_secret=client_secret
        )
        return self.oauth_token 