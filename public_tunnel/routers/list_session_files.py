"""
US-010: AI File Upload Feature - 列出 session 檔案

查看 session 中可用的檔案列表，包含檔案元數據資訊。
"""

from fastapi import APIRouter, HTTPException
from public_tunnel.models.file import SessionFileListResponse
from public_tunnel.dependencies.providers import FileManagerDep

router: APIRouter = APIRouter()


@router.get("/api/sessions/{session_id}/files", response_model=SessionFileListResponse)
async def list_session_files(
    session_id: str,
    file_manager: FileManagerDep
) -> SessionFileListResponse:
    """
    列出指定 session 中的所有檔案
    
    Args:
        session_id: 目標 session ID
        file_manager: 檔案管理服務依賴注入
    
    Returns:
        SessionFileListResponse: session 檔案列表回應
        
    Raises:
        HTTPException: session 不存在時的錯誤回應
    """
    # GREEN Stage 2: Real business logic implementation
    try:
        return file_manager.list_session_files(session_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Session file listing failed: {str(e)}"
        )