"""
US-015: Client Execution Error Reporting Router

Provides error reporting mechanism for clients with same format as success results.
This ensures AI can handle errors consistently through unified result query mechanism.
"""

from datetime import datetime
from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from public_tunnel.models.execution_result import (
    ExecutionResultSubmissionRequest,
    ExecutionResultStatus,
    UnifiedResultQueryResponse
)
from public_tunnel.dependencies.providers import SessionRepositoryDep, ExecutionResultManagerDep

router = APIRouter(tags=["client-execution-error-reporting"])


def _extract_client_id_from_error_context(error_request: ExecutionResultSubmissionRequest, session_id: str) -> str:
    """Extract client_id from error context for unified result storage
    
    In a complete implementation, this would extract the client_id from
    the session context or authentication. For now, uses a test client ID.
    
    Args:
        error_request: Error submission request
        session_id: Session identifier for context
        
    Returns:
        Client identifier for result storage
    """
    # In production: extract from session context or authentication
    return "test-client-error"


# Removed _determine_execution_mode_from_context as CommandExecutionMode is no longer needed


def _build_error_submission_confirmation_response(execution_result) -> Dict[str, Any]:
    """Build unified error submission confirmation response
    
    Creates response format consistent with success result submissions
    to ensure unified handling by AI systems.
    
    Args:
        execution_result: Stored ExecutionResult instance
        
    Returns:
        Confirmation response with unified format
    """
    return {
        "command_id": execution_result.command_id,
        "session_id": execution_result.session_id,
        "execution_status": execution_result.execution_status.value,
        "message": "Error result recorded successfully",
        "submitted_at": execution_result.submitted_at.isoformat()
    }


def _validate_error_result_exists(result_response, command_id: str, session_id: str) -> None:
    """Validate that error result exists in unified storage
    
    Args:
        result_response: Result from unified result manager
        command_id: Command identifier for error message
        session_id: Session identifier for error message
        
    Raises:
        HTTPException: 404 if result not found
    """
    if not result_response:
        raise HTTPException(
            status_code=404,
            detail=f"Error result not found for command '{command_id}' in session '{session_id}'"
        )


def _validate_is_actual_error_result(result_response, command_id: str) -> None:
    """Validate that result is actually an error (not success)
    
    Args:
        result_response: Unified result response to validate
        command_id: Command identifier for error message
        
    Raises:
        HTTPException: 400 if result is not an error
    """
    if result_response.execution_status != ExecutionResultStatus.FAILED:
        raise HTTPException(
            status_code=400,
            detail=f"Command '{command_id}' is not an error result. Status: {result_response.execution_status.value}"
        )


@router.post(
    "/api/sessions/{session_id}/commands/{command_id}/error", 
    summary="Client reports command execution error",
    description="US-015: Client reports execution failures in same format as success results, ensuring AI can handle errors consistently through unified query mechanism."
)
async def report_command_execution_error(
    session_id: str,
    command_id: str,
    error_request: ExecutionResultSubmissionRequest,
    session_repo: SessionRepositoryDep,
    result_manager: ExecutionResultManagerDep
) -> Dict[str, Any]:
    """
    Client reports command execution error with unified format.
    
    US-015 Implementation:
    - Error results use same format as success results  
    - Error results stored with command-id indexing for unified query
    - AI can query errors through same API as success results
    - Consistent error handling across all command types
    
    Args:
        session_id: Target session identifier
        command_id: Failed command identifier
        error_request: Error details in unified result format
        session_repo: Session repository for data validation
        result_manager: Result manager for unified error storage
        
    Returns:
        Dict: Error submission confirmation using unified format
        
    Raises:
        HTTPException: 400 if error_request.execution_status is not FAILED
        HTTPException: 409 if command_id mismatch between path and request
    """
    # API Skeleton Stage: Validate that this is actually an error report
    if error_request.execution_status != ExecutionResultStatus.FAILED:
        raise HTTPException(
            status_code=400,
            detail=f"Error reporting endpoint requires execution_status to be 'failed', got '{error_request.execution_status.value}'"
        )
    
    # Validate command_id consistency
    if error_request.command_id != command_id:
        raise HTTPException(
            status_code=409,
            detail=f"Command ID mismatch: path has '{command_id}', request body has '{error_request.command_id}'"
        )
    
    # Store execution error result through unified result manager
    execution_result = result_manager.create_and_store_result(
        command_id=command_id,
        session_id=session_id,
        client_id=_extract_client_id_from_error_context(error_request, session_id),
        execution_status=ExecutionResultStatus.FAILED,
        error_message=error_request.error_message
    )
    
    return _build_error_submission_confirmation_response(execution_result)


@router.get(
    "/api/sessions/{session_id}/commands/{command_id}/error",
    response_model=UnifiedResultQueryResponse,
    summary="Query command execution error result", 
    description="US-015: Query execution error through unified result mechanism, same API as success results to ensure consistent AI error handling."
)
async def query_command_execution_error(
    session_id: str,
    command_id: str,
    session_repo: SessionRepositoryDep,
    result_manager: ExecutionResultManagerDep
) -> UnifiedResultQueryResponse:
    """
    Query command execution error through unified result mechanism.
    
    US-015 Implementation:
    - Error results queryable through same API as success results
    - Unified result format for both success and error cases
    - Consistent error handling enables AI to process errors uniformly
    - Same command-id indexing mechanism for error results
    
    Args:
        session_id: Target session identifier
        command_id: Failed command identifier to query
        session_repo: Session repository for data retrieval
        result_manager: Result manager for unified error query
        
    Returns:
        UnifiedResultQueryResponse: Error result in same format as success results
        
    Raises:
        HTTPException: 404 if error result not found
        HTTPException: 400 if found result is not an error (execution_status != FAILED)
    """
    # Query error result through unified result mechanism
    unified_result_response = result_manager.get_unified_response(command_id)
    
    _validate_error_result_exists(unified_result_response, command_id, session_id)
    _validate_is_actual_error_result(unified_result_response, command_id)
    
    return unified_result_response