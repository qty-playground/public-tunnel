"""
File - 檔案資料結構

基於 OOA 設計的檔案元數據和存儲管理
"""

from pydantic import BaseModel
from typing import Optional, List, Tuple
from datetime import datetime
from enum import Enum
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


# US-012: Session File Access Isolation Models
class FileAccessDenialReason(str, Enum):
    """檔案存取被拒絕的原因"""
    CROSS_SESSION_ACCESS = "cross_session_access"
    FILE_NOT_FOUND = "file_not_found"  
    SESSION_NOT_EXISTS = "session_not_exists"


class SessionFileAccessValidationRequest(BaseModel):
    """Session 檔案存取驗證請求"""
    requesting_session_id: str
    target_file_id: str
    file_owner_session_id: Optional[str] = None


class SessionFileAccessValidationResponse(BaseModel):
    """Session 檔案存取驗證回應"""
    access_granted: bool
    file_id: str
    requesting_session_id: str
    file_owner_session_id: Optional[str] = None
    denial_reason: Optional[FileAccessDenialReason] = None
    error_message: Optional[str] = None


class CrossSessionAccessDeniedResponse(BaseModel):
    """跨 Session 存取被拒回應模型"""
    error_type: str = "cross_session_access_denied"
    requested_file_id: str
    requesting_session_id: str
    file_owner_session_id: str
    message: str
    timestamp: datetime = datetime.now()


# US-011: Client Result File Upload Models
class ClientResultFileUploadRequest(BaseModel):
    """Client 結果檔案上傳請求模型"""
    file_name: str
    file_content_base64: str  # Base64 編碼的檔案內容
    content_type: Optional[str] = "application/octet-stream"
    file_summary: Optional[str] = None  # Client 可提供檔案摘要


class ClientResultFileUploadResponse(BaseModel):
    """Client 結果檔案上傳回應模型"""
    file_id: str
    file_name: str
    session_id: str
    upload_timestamp: datetime
    file_size_bytes: int
    content_type: str
    file_summary: Optional[str] = None


class ClientResultFileMetadataResponse(BaseModel):
    """Client 結果檔案元數據回應模型"""
    file_id: str
    file_name: str
    content_type: str
    file_size_bytes: int
    upload_timestamp: datetime
    file_summary: Optional[str] = None


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


# US-022: File Unique Identification Models
class FileUniqueIdentificationRequest(BaseModel):
    """檔案唯一識別請求模型"""
    filename: Optional[str] = None
    min_size_bytes: Optional[int] = None
    max_size_bytes: Optional[int] = None
    content_type: Optional[str] = None
    uploaded_after: Optional[datetime] = None
    uploaded_before: Optional[datetime] = None


class FileUniqueIdentificationResponse(BaseModel):
    """檔案唯一識別回應模型"""
    session_id: str
    total_matching_files: int
    files: List[FileMetadataResponse]
    duplicate_filename_groups: List[str]  # 有重複的檔名列表


class FileDuplicateGroup(BaseModel):
    """重複檔名群組模型"""
    filename: str
    duplicate_count: int
    files: List[FileMetadataResponse]


class DuplicateFilenameAnalysisResponse(BaseModel):
    """重複檔名分析回應模型"""
    session_id: str
    total_unique_filenames: int
    total_duplicate_groups: int
    duplicate_groups: List[FileDuplicateGroup]


class FileComparisonRequest(BaseModel):
    """檔案比較請求模型"""
    file_ids: List[str]


class FileComparisonItem(BaseModel):
    """檔案比較項目模型"""
    file_id: str
    file_name: str
    file_size_bytes: int
    content_type: str
    upload_timestamp: datetime
    file_summary: Optional[str] = None
    content_hash: Optional[str] = None  # MD5 或 SHA256 hash


class FileComparisonResponse(BaseModel):
    """檔案比較回應模型"""
    session_id: str
    comparison_count: int
    files: List[FileComparisonItem]
    identical_content_pairs: List[Tuple[str, str]]  # (file_id1, file_id2) 內容相同的檔案對
    same_filename_count: int


class EnhancedFileMetadataResponse(BaseModel):
    """增強版檔案 metadata 回應模型"""
    file_id: str
    file_name: str
    content_type: str
    file_size_bytes: int
    upload_timestamp: datetime
    file_summary: Optional[str] = None
    content_hash: str  # 檔案內容的 hash
    same_filename_count_in_session: int  # 同 session 中相同檔名的檔案數量
    is_content_unique_in_session: bool  # 在 session 中檔案內容是否唯一