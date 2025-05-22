from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime

@dataclass
class RequestModel:
    method: str = "GET"
    url: str = ""
    params: Dict[str, str] = field(default_factory=dict)
    headers: Dict[str, str] = field(default_factory=dict)
    body_type: str = "none"  # none, raw, json, form
    body_content: str = ""
    form_data: Dict[str, str] = field(default_factory=dict)
    auth_type: str = "none"  # none, basic, bearer, oauth1, oauth2
    auth_data: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Convert the request model to a dictionary for saving"""
        return {
            'method': self.method,
            'url': self.url,
            'params': [{'key': k, 'value': v} for k, v in self.params.items()],
            'headers': [{'key': k, 'value': v} for k, v in self.headers.items()],
            'body_type': self.body_type,
            'body_content': self.body_content,
            'form_data': [{'key': k, 'value': v} for k, v in self.form_data.items()],
            'auth_type': self.auth_type,
            'auth_data': self.auth_data
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'RequestModel':
        """Create a request model from a dictionary"""
        params = {item['key']: item['value'] for item in data.get('params', [])}
        headers = {item['key']: item['value'] for item in data.get('headers', [])}
        form_data = {item['key']: item['value'] for item in data.get('form_data', [])}
        
        return cls(
            method=data.get('method', 'GET'),
            url=data.get('url', ''),
            params=params,
            headers=headers,
            body_type=data.get('body_type', 'none'),
            body_content=data.get('body_content', ''),
            form_data=form_data,
            auth_type=data.get('auth_type', 'none'),
            auth_data=data.get('auth_data', {})
        ) 