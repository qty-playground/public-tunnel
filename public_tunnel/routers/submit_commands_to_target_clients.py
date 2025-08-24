"""
Submit commands to target clients - US-006 Implementation

Handles targeted command submission functionality for specific clients within sessions.
This is the core implementation for US-006: Targeted Client Command Submission.
"""

from fastapi import APIRouter, HTTPException
from public_tunnel.models.command import (
    SubmitCommandToTargetClientRequest, 
    CommandSubmissionToTargetResponse
)
from public_tunnel.dependencies.providers import (
    SessionRepositoryDep, 
    CommandValidatorDep,
    CommandQueueManagerDep
)

router: APIRouter = APIRouter(tags=["targeted-command-submission"])


@router.post("/api/sessions/{session_id}/commands/submit", response_model=CommandSubmissionToTargetResponse)
async def submit_command_to_target_client_in_session(
    session_id: str,
    command_request: SubmitCommandToTargetClientRequest,
    session_repo: SessionRepositoryDep,
    command_validator: CommandValidatorDep,
    command_queue_manager: CommandQueueManagerDep
) -> CommandSubmissionToTargetResponse:
    """
    Submit command to a specific target client within a session
    
    Core functionality for US-006: Targeted Client Command Submission
    - Command is queued for specific target client only
    - Only the target client will receive this command during polling
    - FIFO queue management ensures fair command processing
    
    Args:
        session_id: The session identifier where the command will be submitted
        command_request: Command details including content and target client
        session_repo: Session repository for data persistence
        command_validator: Command validation service
        
    Returns:
        CommandSubmissionToTargetResponse: Command submission confirmation with details
        
    Raises:
        HTTPException: 501 Not Implemented during API skeleton phase
    """
    # GREEN Stage 2: Real implementation with command queue management
    from datetime import datetime
    from public_tunnel.models.command import CommandExecutionStatus
    
    # Submit command to target client's queue using queue manager
    command = command_queue_manager.submit_command_to_target_client(
        session_id=session_id,
        target_client_id=command_request.target_client_id,
        command_content=command_request.command_content
    )
    
    # Return response with real command information
    return CommandSubmissionToTargetResponse(
        command_id=command.command_id,
        execution_status=CommandExecutionStatus.PENDING,
        submission_timestamp=datetime.now(),
        target_client_id=command_request.target_client_id,
        estimated_completion_time=None  # Will be estimated after queue processing
    )