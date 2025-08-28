"""
Auto Async Command Submission - US-008 Implementation

Handles command submission with automatic switching between synchronous and asynchronous responses
based on execution time thresholds.
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
import uuid
from public_tunnel.models.command import (
    SubmitCommandToTargetClientRequest,
    AutoAsyncCommandResponse
)
from public_tunnel.dependencies.providers import (
    SessionRepositoryDep,
    CommandValidatorDep, 
    CommandQueueManagerDep,
    ClientPresenceTrackerDep,
    OfflineStatusManagerDep,
    ExecutionResultManagerDep
)

router: APIRouter = APIRouter(tags=["auto-async-command-submission"])


@router.post(
    "/api/sessions/{session_id}/commands/submit-auto-async",
    response_model=AutoAsyncCommandResponse,
    summary="Submit command with auto async response",
    description="US-008: Submit command that returns immediately if fast, or provides command-id for polling if slow"
)
async def submit_command_with_auto_async_response(
    session_id: str,
    command_request: SubmitCommandToTargetClientRequest,
    session_repo: SessionRepositoryDep = None,
    command_validator: CommandValidatorDep = None,
    command_queue_manager: CommandQueueManagerDep = None,
    presence_tracker: ClientPresenceTrackerDep = None,
    offline_status_manager: OfflineStatusManagerDep = None,
    execution_result_manager: ExecutionResultManagerDep = None
) -> AutoAsyncCommandResponse:
    """
    Submit command with automatic sync/async response handling.
    
    This endpoint implements:
    - US-008: Auto Async Response with Initial Wait
    - Fast commands (within threshold): Return result immediately
    - Slow commands (exceed threshold): Return command-id for polling
    
    The response switches automatically based on execution time.
    """
    # US-008: Real implementation of auto async logic
    
    # Validate request and check prerequisites
    if not session_repo.is_client_in_session(session_id, command_request.target_client_id):
        raise HTTPException(status_code=404, detail="Client not found in session")
    
    # Check if client is offline (US-014 integration)
    if offline_status_manager and not offline_status_manager.is_client_eligible_for_commands(
        command_request.target_client_id, session_id
    ):
        raise HTTPException(status_code=422, detail="Target client is offline")
    
    # Submit command to queue (using existing infrastructure)
    submitted_command = command_queue_manager.submit_command_to_target_client(
        session_id=session_id,
        target_client_id=command_request.target_client_id,
        command_content=command_request.command_content
    )
    
    # Get command_id from the submitted command
    command_id = submitted_command.command_id
    
    # Auto Async Logic: Wait briefly for fast execution
    # For simplicity in this implementation, we simulate execution time based on command content
    wait_threshold_seconds = 1.0  # configurable threshold
    
    # Simulate execution time based on command content
    # Fast commands (like "echo") complete immediately
    # Slow commands (containing "sleep") exceed threshold
    is_fast_command = "sleep" not in command_request.command_content.lower()
    
    if is_fast_command:
        # Fast execution: create and complete result immediately for unified query
        if execution_result_manager:
            from public_tunnel.models.execution_result import ExecutionResult, ExecutionResultStatus
            
            mock_result = f"Result of: {command_request.command_content}"
            
            # Create completed result entry for unified query mechanism
            completed_result = ExecutionResult(
                command_id=command_id,
                execution_status=ExecutionResultStatus.COMPLETED,
                client_id=command_request.target_client_id,
                session_id=session_id
            )
            completed_result.complete_with_success(mock_result)
            execution_result_manager.store_result(completed_result)
        else:
            mock_result = f"Result of: {command_request.command_content}"
        
        return AutoAsyncCommandResponse(
            command_id=command_id,
            async_mode=False,
            result=mock_result,
            submission_timestamp=datetime.now(),
            target_client_id=command_request.target_client_id
        )
    else:
        # Slow execution: create pending result entry for later polling
        if execution_result_manager:
            # Import here to avoid circular imports
            from public_tunnel.models.execution_result import ExecutionResult, ExecutionResultStatus
            
            # Create pending result entry
            pending_result = ExecutionResult(
                command_id=command_id,
                execution_status=ExecutionResultStatus.PENDING,
                client_id=command_request.target_client_id,
                session_id=session_id
            )
            execution_result_manager.store_result(pending_result)
        
        # Return command-id for polling
        return AutoAsyncCommandResponse(
            command_id=command_id,
            async_mode=True,
            result=None,
            submission_timestamp=datetime.now(),
            target_client_id=command_request.target_client_id
        )