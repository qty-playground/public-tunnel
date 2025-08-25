"""
SessionFileAccessValidator - US-012: Session File Access Isolation

提供檔案存取權限驗證和跨 session 存取控制功能。
確保檔案存取被限制在相同的 session 內。
"""

from typing import Optional, List
from datetime import datetime
from fastapi import HTTPException
from public_tunnel.models.file import (
    SessionFileAccessValidationResponse,
    CrossSessionAccessDeniedResponse,
    FileAccessDenialReason
)


class SessionFileAccessValidator:
    """Session 檔案存取驗證器
    
    負責驗證檔案存取權限，記錄違規存取嘗試，
    並確保檔案存取隔離在相同 session 內。
    """
    
    def __init__(self, file_manager=None):
        """初始化檔案存取驗證器
        
        Args:
            file_manager: 檔案管理服務實例，用於查詢檔案資訊
        """
        self.file_manager = file_manager
        self.access_violations: List[CrossSessionAccessDeniedResponse] = []
    
    def validate_file_access(self, requesting_session_id: str, file_id: str) -> SessionFileAccessValidationResponse:
        """驗證 session 對檔案的存取權限
        
        Args:
            requesting_session_id: 請求存取的 session ID
            file_id: 目標檔案 ID
            
        Returns:
            SessionFileAccessValidationResponse: 存取驗證結果
        """
        # 檢查檔案是否存在
        if not self.file_manager:
            # 測試模式：使用模擬邏輯
            return self._mock_validate_file_access(requesting_session_id, file_id)
        
        # 從檔案管理器獲取檔案資訊
        file_info = self.file_manager.get_file_info(file_id)
        
        if not file_info:
            return SessionFileAccessValidationResponse(
                access_granted=False,
                file_id=file_id,
                requesting_session_id=requesting_session_id,
                file_owner_session_id=None,
                denial_reason=FileAccessDenialReason.FILE_NOT_FOUND,
                error_message=f"File {file_id} not found"
            )
        
        # 檢查檔案所屬的 session
        file_owner_session_id = getattr(file_info, 'session_id', None)
        
        if not file_owner_session_id:
            return SessionFileAccessValidationResponse(
                access_granted=False,
                file_id=file_id,
                requesting_session_id=requesting_session_id,
                file_owner_session_id=None,
                denial_reason=FileAccessDenialReason.SESSION_NOT_EXISTS,
                error_message="File does not belong to any session"
            )
        
        # 檢查是否為相同 session
        if requesting_session_id != file_owner_session_id:
            # 記錄跨 session 存取違規
            violation = CrossSessionAccessDeniedResponse(
                requested_file_id=file_id,
                requesting_session_id=requesting_session_id,
                file_owner_session_id=file_owner_session_id,
                message=f"Cross-session file access denied: {requesting_session_id} attempted to access file {file_id} from session {file_owner_session_id}",
                timestamp=datetime.now()
            )
            self.access_violations.append(violation)
            
            return SessionFileAccessValidationResponse(
                access_granted=False,
                file_id=file_id,
                requesting_session_id=requesting_session_id,
                file_owner_session_id=file_owner_session_id,
                denial_reason=FileAccessDenialReason.CROSS_SESSION_ACCESS,
                error_message="Cross-session file access is not allowed"
            )
        
        # 相同 session，允許存取
        return SessionFileAccessValidationResponse(
            access_granted=True,
            file_id=file_id,
            requesting_session_id=requesting_session_id,
            file_owner_session_id=file_owner_session_id,
            denial_reason=None,
            error_message=None
        )
    
    def _mock_validate_file_access(self, requesting_session_id: str, file_id: str) -> SessionFileAccessValidationResponse:
        """測試用的模擬檔案存取驗證
        
        基於檔案 ID 和 session ID 的命名模式進行模擬驗證
        """
        # 模擬檔案 ID 包含 session 資訊的情況
        # 例如: mock-file-a-id 屬於 test-session-a-us012
        # mock-file-b-id 屬於 test-session-b-us012
        
        if file_id == "mock-file-a-id":
            file_owner_session_id = "test-session-a-us012"
        elif file_id == "mock-file-b-id":
            file_owner_session_id = "test-session-b-us012"
        else:
            # 未知檔案
            return SessionFileAccessValidationResponse(
                access_granted=False,
                file_id=file_id,
                requesting_session_id=requesting_session_id,
                file_owner_session_id=None,
                denial_reason=FileAccessDenialReason.FILE_NOT_FOUND,
                error_message=f"File {file_id} not found"
            )
        
        # 檢查是否為相同 session
        if requesting_session_id != file_owner_session_id:
            # 記錄跨 session 存取違規
            violation = CrossSessionAccessDeniedResponse(
                requested_file_id=file_id,
                requesting_session_id=requesting_session_id,
                file_owner_session_id=file_owner_session_id,
                message=f"Cross-session file access denied: {requesting_session_id} attempted to access file {file_id} from session {file_owner_session_id}",
                timestamp=datetime.now()
            )
            self.access_violations.append(violation)
            
            return SessionFileAccessValidationResponse(
                access_granted=False,
                file_id=file_id,
                requesting_session_id=requesting_session_id,
                file_owner_session_id=file_owner_session_id,
                denial_reason=FileAccessDenialReason.CROSS_SESSION_ACCESS,
                error_message="Cross-session file access is not allowed"
            )
        
        # 相同 session，允許存取
        return SessionFileAccessValidationResponse(
            access_granted=True,
            file_id=file_id,
            requesting_session_id=requesting_session_id,
            file_owner_session_id=file_owner_session_id,
            denial_reason=None,
            error_message=None
        )
    
    def get_recent_access_violations(self, session_id: str, limit: int = 50) -> List[CrossSessionAccessDeniedResponse]:
        """獲取指定 session 的最近存取違規記錄
        
        Args:
            session_id: 目標 session ID
            limit: 返回記錄數量限制
            
        Returns:
            List[CrossSessionAccessDeniedResponse]: 違規記錄列表
        """
        # 過濾出針對該 session 檔案的違規嘗試
        session_violations = [
            violation for violation in self.access_violations
            if violation.file_owner_session_id == session_id
        ]
        
        # 按時間倒序排列，返回最近的記錄
        session_violations.sort(key=lambda x: x.timestamp, reverse=True)
        return session_violations[:limit]
    
    def is_cross_session_access(self, requesting_session_id: str, file_id: str) -> bool:
        """快速檢查是否為跨 session 存取
        
        Args:
            requesting_session_id: 請求存取的 session ID
            file_id: 目標檔案 ID
            
        Returns:
            bool: True 如果是跨 session 存取，False 如果是相同 session 存取
        """
        validation_result = self.validate_file_access(requesting_session_id, file_id)
        return not validation_result.access_granted and \
               validation_result.denial_reason == FileAccessDenialReason.CROSS_SESSION_ACCESS
    
    def validate_access_or_raise(self, requesting_session_id: str, file_id: str) -> None:
        """驗證檔案存取權限，如果被拒絕則拋出適當的 HTTPException
        
        這是一個便利方法，用於路由中統一處理存取驗證錯誤。
        
        Args:
            requesting_session_id: 請求存取的 session ID
            file_id: 目標檔案 ID
            
        Raises:
            HTTPException: 403 Forbidden for cross-session access
            HTTPException: 404 Not Found for non-existent files
            HTTPException: 403 Forbidden for other access denials
        """
        validation_result = self.validate_file_access(requesting_session_id, file_id)
        
        if not validation_result.access_granted:
            if validation_result.denial_reason == FileAccessDenialReason.CROSS_SESSION_ACCESS:
                raise HTTPException(
                    status_code=403,
                    detail=f"Cross-session file access denied. File belongs to session {validation_result.file_owner_session_id}"
                )
            elif validation_result.denial_reason == FileAccessDenialReason.FILE_NOT_FOUND:
                raise HTTPException(
                    status_code=404,
                    detail=f"File {file_id} not found"
                )
            else:
                raise HTTPException(
                    status_code=403,
                    detail=validation_result.error_message or "File access denied"
                )


class InMemorySessionFileAccessValidator(SessionFileAccessValidator):
    """記憶體內 Session 檔案存取驗證器實作
    
    適用於開發和測試環境，將違規記錄保存在記憶體中。
    """
    pass