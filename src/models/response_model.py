from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

@dataclass
class ResponseModel:
    status_code: int
    reason: str
    headers: dict
    content: bytes
    elapsed_time: float  # in milliseconds
    timestamp: datetime = field(default_factory=datetime.now)
    error: Optional[str] = None
    
    @property
    def is_success(self) -> bool:
        return 200 <= self.status_code < 300
    
    @property
    def is_json(self) -> bool:
        return self.headers.get('content-type', '').startswith('application/json')
    
    @property
    def size(self) -> int:
        return len(self.content)
    
    @property
    def size_formatted(self) -> str:
        """Get formatted size (bytes, KB)"""
        size = self.size
        if size > 1024:
            return f"{round(size / 1024, 2)} KB"
        return f"{size} bytes"
    
    @classmethod
    def from_error(cls, error: Exception) -> 'ResponseModel':
        """Create an error response"""
        return cls(
            status_code=0,
            reason="Error",
            headers={},
            content=b"",
            elapsed_time=0,
            error=str(error)
        ) 