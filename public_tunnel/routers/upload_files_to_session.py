"""
US-010: AI File Upload Feature - 上傳檔案到 session

AI 可以上傳檔案到 session，檔案會獲得 unique file-id，
session 中的 clients 可以下載這些檔案。
"""

from fastapi import APIRouter, HTTPException
from public_tunnel.models.file import FileUploadRequest, FileUploadResponse
from public_tunnel.dependencies.providers import FileManagerDep

router: APIRouter = APIRouter()


@router.post("/api/sessions/{session_id}/files", response_model=FileUploadResponse)
async def upload_file_to_session(
    session_id: str,
    file_request: FileUploadRequest,
    file_manager: FileManagerDep
) -> FileUploadResponse:
    """
    AI 上傳檔案到指定 session
    
    Args:
        session_id: 目標 session ID
        file_request: 檔案上傳請求（包含檔案名稱、內容、類型等）
        file_manager: 檔案管理服務依賴注入
    
    Returns:
        FileUploadResponse: 上傳成功回應（包含 file-id）
        
    Raises:
        HTTPException: 上傳失敗時的錯誤回應
    """
    # GREEN Stage 2: Real business logic implementation
    try:
        return file_manager.upload_file_to_session(session_id, file_request)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file upload request: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"File upload failed: {str(e)}"
        )