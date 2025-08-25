"""
US-010: AI File Upload Feature - 從 session 下載檔案

Clients 和 AI 可以從 session 下載檔案，透過 unique file-id 識別檔案。
"""

from fastapi import APIRouter, HTTPException
from public_tunnel.models.file import FileDownloadResponse
from public_tunnel.dependencies.providers import FileManagerDep

router: APIRouter = APIRouter()


@router.get("/api/sessions/{session_id}/files/{file_id}", response_model=FileDownloadResponse)
async def download_file_from_session(
    session_id: str,
    file_id: str,
    file_manager: FileManagerDep
) -> FileDownloadResponse:
    """
    從指定 session 下載檔案
    
    Args:
        session_id: 目標 session ID
        file_id: 檔案 unique ID
        file_manager: 檔案管理服務依賴注入
    
    Returns:
        FileDownloadResponse: 檔案下載回應（包含檔案內容）
        
    Raises:
        HTTPException: 檔案不存在或權限不足時的錯誤回應
    """
    # GREEN Stage 2: Real business logic implementation
    try:
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