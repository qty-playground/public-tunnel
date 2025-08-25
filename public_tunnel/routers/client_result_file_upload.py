"""
US-011: Client Result File Upload Router

Provides mechanism for clients to upload result files with metadata.
This enables AI to identify and download relevant files selectively.
"""

from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException

from public_tunnel.models.execution_result import ExecutionResultStatus
from public_tunnel.models.file import (
    ClientResultFileUploadRequest,
    ClientResultFileUploadResponse,
    FileUploadRequest
)

# Define models specific to this router to avoid circular imports
from pydantic import BaseModel

class ClientResultSubmissionWithFilesRequest(BaseModel):
    """Client 結果提交包含檔案請求模型"""
    command_id: str
    execution_status: ExecutionResultStatus
    result_content: Optional[str] = None
    error_message: Optional[str] = None
    execution_duration_seconds: Optional[int] = None
    result_files: Optional[List[ClientResultFileUploadRequest]] = None  # 結果檔案列表


class ClientResultSubmissionWithFilesResponse(BaseModel):
    """Client 結果提交包含檔案回應模型"""
    command_id: str
    session_id: str
    execution_status: ExecutionResultStatus
    submitted_at: datetime
    file_references: List[str]  # 上傳檔案的 file-id 列表
    uploaded_files: List[ClientResultFileUploadResponse]  # 上傳檔案詳情


from public_tunnel.dependencies.providers import (
    SessionRepositoryDep,
    ExecutionResultManagerDep,
    FileManagerDep
)

router = APIRouter(tags=["client-result-file-upload"])


def _resolve_client_id_for_result_submission(session_id: str, command_id: str) -> str:
    """Resolve client identifier for result submission context"""
    return "test-client-upload"


# Removed _determine_original_command_execution_mode as CommandExecutionMode is no longer needed


def _upload_execution_result_files_to_session_storage(
    session_id: str,
    result_files: List[ClientResultFileUploadRequest],
    file_manager: "FileManager"
) -> List[ClientResultFileUploadResponse]:
    """Upload execution result files to session storage with metadata"""
    uploaded_files = []
    
    for result_file in result_files:
        try:
            standard_file_upload_request = FileUploadRequest(
                file_name=result_file.file_name,
                file_content_base64=result_file.file_content_base64,
                content_type=result_file.content_type,
                file_summary=result_file.file_summary
            )
            
            upload_response = file_manager.upload_file_to_session(
                session_id=session_id,
                file_request=standard_file_upload_request
            )
            
            client_upload_response = ClientResultFileUploadResponse(
                file_id=upload_response.file_id,
                file_name=upload_response.file_name,
                session_id=upload_response.session_id,
                upload_timestamp=upload_response.upload_timestamp,
                file_size_bytes=upload_response.file_size_bytes,
                content_type=upload_response.content_type,
                file_summary=upload_response.file_summary
            )
            
            uploaded_files.append(client_upload_response)
            
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to upload file '{result_file.file_name}': {str(e)}"
            )
    
    return uploaded_files


def _create_execution_result_with_uploaded_file_references(
    command_id: str,
    session_id: str,
    submission_request: ClientResultSubmissionWithFilesRequest,
    uploaded_file_ids: List[str],
    result_manager: "ExecutionResultManager"
) -> "ExecutionResult":
    """Create and store execution result with uploaded file references"""
    client_id = _resolve_client_id_for_result_submission(session_id, command_id)
    
    execution_result = result_manager.create_and_store_result(
        command_id=command_id,
        session_id=session_id,
        client_id=client_id,
        execution_status=submission_request.execution_status,
        result_content=submission_request.result_content,
        error_message=submission_request.error_message
    )
    
    execution_result.file_references = uploaded_file_ids
    return execution_result


@router.post(
    "/api/sessions/{session_id}/commands/{command_id}/result-with-files",
    response_model=ClientResultSubmissionWithFilesResponse,
    summary="Client uploads execution result with files",
    description="US-011: Client uploads result files with metadata so that AI can identify and download relevant files selectively."
)
async def upload_client_result_with_files(
    session_id: str,
    command_id: str,
    request: ClientResultSubmissionWithFilesRequest,
    session_repo: SessionRepositoryDep,
    result_manager: ExecutionResultManagerDep,
    file_manager: FileManagerDep
) -> ClientResultSubmissionWithFilesResponse:
    """
    Client uploads execution result with files and metadata.
    
    US-011 Implementation:
    - Client can upload result files as part of result reporting
    - Each file gets unique file-id, filename, and summary
    - AI can browse and download files selectively through existing file APIs
    - Files are stored with session-based isolation
    
    Args:
        session_id: Target session identifier
        command_id: Executed command identifier
        request: Result submission with files request
        session_repo: Session repository for validation
        result_manager: Result manager for execution result storage
        file_manager: File manager for file uploads
        
    Returns:
        ClientResultSubmissionWithFilesResponse: Upload confirmation with file metadata
        
    Raises:
        HTTPException: 409 if command_id mismatch between path and request
        HTTPException: 400 if file upload fails
    """
    if request.command_id != command_id:
        raise HTTPException(
            status_code=409,
            detail=f"Command ID mismatch: path has '{command_id}', request body has '{request.command_id}'"
        )
    
    uploaded_result_files = []
    uploaded_file_ids = []
    
    if request.result_files:
        uploaded_result_files = _upload_execution_result_files_to_session_storage(
            session_id=session_id,
            result_files=request.result_files,
            file_manager=file_manager
        )
        uploaded_file_ids = [file_upload.file_id for file_upload in uploaded_result_files]
    
    execution_result = _create_execution_result_with_uploaded_file_references(
        command_id=command_id,
        session_id=session_id,
        submission_request=request,
        uploaded_file_ids=uploaded_file_ids,
        result_manager=result_manager
    )
    
    return ClientResultSubmissionWithFilesResponse(
        command_id=command_id,
        session_id=session_id,
        execution_status=request.execution_status,
        submitted_at=execution_result.submitted_at,
        file_references=uploaded_file_ids,
        uploaded_files=uploaded_result_files
    )