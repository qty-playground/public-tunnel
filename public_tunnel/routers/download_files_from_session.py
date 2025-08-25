"""
US-010: AI File Upload Feature - 從 session 下載檔案
US-012: Session File Access Isolation - 增強版本

Clients 和 AI 可以從 session 下載檔案，透過 unique file-id 識別檔案。
此版本包含 US-012 的 session 隔離檢查功能。
"""

from fastapi import APIRouter, HTTPException
from public_tunnel.models.file import FileDownloadResponse, CrossSessionAccessDeniedResponse
from public_tunnel.dependencies.providers import FileManagerDep, SessionFileAccessValidatorDep

router: APIRouter = APIRouter()


@router.get("/api/sessions/{session_id}/files/{file_id}", response_model=FileDownloadResponse)
async def download_file_from_session(
    session_id: str,
    file_id: str,
    file_manager: FileManagerDep,
    access_validator: SessionFileAccessValidatorDep
) -> FileDownloadResponse:
    """
    從指定 session 下載檔案 - 增強版本包含 session 隔離檢查
    
    此端點結合了 US-010 的檔案下載功能和 US-012 的 session 隔離保護。
    會先驗證請求的 session 是否有權限存取目標檔案。
    
    Args:
        session_id: 目標 session ID
        file_id: 檔案 unique ID
        file_manager: 檔案管理服務依賴注入
        access_validator: session 存取驗證服務依賴注入
    
    Returns:
        FileDownloadResponse: 檔案下載回應（包含檔案內容）
        
    Raises:
        HTTPException: 403 Forbidden for cross-session access attempts
        HTTPException: 404 Not Found for non-existent files
        HTTPException: 500 Internal Server Error for other failures
    """
    # US-010: Original file download functionality (preserved)
    # US-012: Add session isolation validation
    
    try:
        # First validate session access permissions (US-012) - unified error handling
        access_validator.validate_access_or_raise(session_id, file_id)
        
        # Access validated, proceed with file download (US-010)
        file_response = file_manager.download_file_from_session(session_id, file_id)
        
        if file_response is None:
            raise HTTPException(
                status_code=404,
                detail=f"File {file_id} not found in session {session_id}"
            )
        
        return file_response
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"File download failed: {str(e)}"
        )