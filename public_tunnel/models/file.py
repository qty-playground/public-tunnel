"""
File - 檔案資料結構

基於 OOA 設計的檔案元數據和存儲管理
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid


class FileUploadRequest(BaseModel):
    """AI 上傳檔案到 session 的請求模型"""
    file_name: str
    file_content_base64: str  # Base64 編碼的檔案內容
    content_type: Optional[str] = "application/octet-stream"
    file_summary: Optional[str] = None  # AI 可提供檔案摘要


class FileUploadResponse(BaseModel):
    """檔案上傳回應模型"""
    file_id: str
    file_name: str
    session_id: str
    upload_timestamp: datetime
    file_size_bytes: int
    content_type: str
    file_summary: Optional[str] = None


class FileDownloadResponse(BaseModel):
    """檔案下載回應模型"""
    file_id: str
    file_name: str
    file_content_base64: str  # Base64 編碼的檔案內容
    content_type: str
    file_size_bytes: int
    upload_timestamp: datetime
    file_summary: Optional[str] = None


class FileMetadataResponse(BaseModel):
    """檔案元數據回應模型"""
    file_id: str
    file_name: str
    content_type: str
    file_size_bytes: int
    upload_timestamp: datetime
    file_summary: Optional[str] = None


class SessionFileListResponse(BaseModel):
    """Session 檔案列表回應模型"""
    session_id: str
    total_files: int
    files: List[FileMetadataResponse]


class File:
    """檔案資料結構 - 基於 OOA 設計"""
    
    def __init__(self, file_name: str, content: bytes, session_id: str, 
                 content_type: str = "application/octet-stream", 
                 file_summary: Optional[str] = None):
        self.file_id = str(uuid.uuid4())
        self.file_name = file_name
        self.content = content
        self.session_id = session_id
        self.content_type = content_type
        self.file_summary = file_summary or self.generate_summary()
        self.created_time = datetime.now().timestamp()
    
    def get_unique_id(self) -> str:
        """取得唯一ID"""
        return self.file_id
    
    def get_summary(self) -> str:
        """取得摘要"""
        return self.file_summary or "No summary available"
    
    def get_size(self) -> int:
        """取得檔案大小"""
        return len(self.content)
    
    def belongs_to_session(self, session_id: str) -> bool:
        """Session 歸屬檢查"""
        return self.session_id == session_id
    
    def generate_summary(self) -> str:
        """自動生成摘要"""
        size = self.get_size()
        if size < 1024:
            size_str = f"{size} bytes"
        elif size < 1024 * 1024:
            size_str = f"{size // 1024} KB"
        else:
            size_str = f"{size // (1024 * 1024)} MB"
        
        return f"{self.file_name} ({size_str}, {self.content_type})"
    
    def to_metadata_response(self) -> FileMetadataResponse:
        """轉換為檔案元數據回應格式"""
        return FileMetadataResponse(
            file_id=self.file_id,
            file_name=self.file_name,
            content_type=self.content_type,
            file_size_bytes=self.get_size(),
            upload_timestamp=datetime.fromtimestamp(self.created_time),
            file_summary=self.file_summary
        )
    
    def to_json(self) -> dict:
        """序列化為 JSON（不含 content）"""
        return {
            "file_id": self.file_id,
            "file_name": self.file_name,
            "session_id": self.session_id,
            "content_type": self.content_type,
            "file_size_bytes": self.get_size(),
            "created_time": self.created_time,
            "file_summary": self.file_summary
        }