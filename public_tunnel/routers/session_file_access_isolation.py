"""
US-012: Session File Access Isolation

確保檔案存取被限制在相同的 session 內，防止跨 session 存取檔案。
提供檔案存取驗證機制和錯誤處理。
"""

from fastapi import APIRouter, HTTPException
from public_tunnel.models.file import (
    SessionFileAccessValidationRequest,
    SessionFileAccessValidationResponse,
    CrossSessionAccessDeniedResponse,
    FileAccessDenialReason
)
from public_tunnel.dependencies.providers import SessionFileAccessValidatorDep, FileManagerDep

router: APIRouter = APIRouter()


@router.post("/api/sessions/{session_id}/files/{file_id}/validate-access", 
             response_model=SessionFileAccessValidationResponse)
async def validate_session_file_access(
    session_id: str,
    file_id: str,
    access_validator: SessionFileAccessValidatorDep
) -> SessionFileAccessValidationResponse:
    """
    驗證 session 對檔案的存取權限
    
    Args:
        session_id: 請求存取的 session ID
        file_id: 目標檔案 ID
        access_validator: 存取驗證服務依賴注入
    
    Returns:
        SessionFileAccessValidationResponse: 存取驗證結果
        
    Raises:
        HTTPException: 驗證服務不可用時的錯誤回應
    """
    try:
        validation_result = access_validator.validate_file_access(session_id, file_id)
        return validation_result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"File access validation failed: {str(e)}"
        )


@router.get("/api/sessions/{session_id}/files/{file_id}/secure-download")
async def download_file_with_session_isolation_check(
    session_id: str,
    file_id: str,
    access_validator: SessionFileAccessValidatorDep,
    file_manager: FileManagerDep
):
    """
    下載檔案並強制執行 session 隔離檢查
    
    這個端點增強現有的檔案下載功能，加入嚴格的 session 隔離驗證。
    與 US-010 的一般下載端點不同，此端點會明確拒絕跨 session 存取。
    
    Args:
        session_id: 請求存取的 session ID
        file_id: 目標檔案 ID
        access_validator: 存取驗證服務依賴注入
        file_manager: 檔案管理服務依賴注入
    
    Returns:
        FileDownloadResponse: 檔案下載回應（僅限相同 session）
        
    Raises:
        HTTPException: 403 Forbidden for cross-session access
        HTTPException: 404 Not Found for non-existent files
    """
    try:
        # 嚴格的 session 隔離檢查 - unified error handling
        access_validator.validate_access_or_raise(session_id, file_id)
        
        # 驗證通過，執行安全下載
        file_response = file_manager.download_file_from_session(session_id, file_id)
        
        if file_response is None:
            raise HTTPException(
                status_code=404,
                detail=f"File {file_id} not found in session {session_id}"
            )
        
        return file_response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Secure file download failed: {str(e)}"
        )


@router.get("/api/sessions/{session_id}/access-violations", 
           response_model=list[CrossSessionAccessDeniedResponse])
async def list_recent_cross_session_access_violations(
    session_id: str,
    access_validator: SessionFileAccessValidatorDep
) -> list[CrossSessionAccessDeniedResponse]:
    """
    列出最近的跨 session 存取違規記錄
    
    此端點提供安全審核功能，讓管理員或 session 擁有者
    可以檢視是否有其他 session 嘗試存取此 session 的檔案。
    
    Args:
        session_id: 目標 session ID
        access_validator: 存取驗證服務依賴注入
    
    Returns:
        List[CrossSessionAccessDeniedResponse]: 違規記錄列表
        
    Raises:
        HTTPException: 服務不可用時的錯誤回應
    """
    try:
        violations = access_validator.get_recent_access_violations(session_id)
        return violations
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Access violation retrieval failed: {str(e)}"
        )