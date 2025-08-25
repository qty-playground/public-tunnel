"""
Submit commands to target clients - US-006 Implementation

Handles targeted command submission functionality for specific clients within sessions.
This is the core implementation for US-006: Targeted Client Command Submission.
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from public_tunnel.models.command import (
    SubmitCommandToTargetClientRequest, 
    CommandSubmissionToTargetResponse,
    CommandExecutionStatus
)
from public_tunnel.dependencies.providers import (
    SessionRepositoryDep, 
    CommandValidatorDep,
    CommandQueueManagerDep,
    ClientPresenceTrackerDep,
    OfflineStatusManagerDep
)

router: APIRouter = APIRouter(tags=["targeted-command-submission"])


@router.post("/api/sessions/{session_id}/commands/submit", response_model=CommandSubmissionToTargetResponse)
async def submit_command_to_target_client_in_session(
    session_id: str,
    command_request: SubmitCommandToTargetClientRequest,
    session_repo: SessionRepositoryDep,
    command_validator: CommandValidatorDep,
    command_queue_manager: CommandQueueManagerDep,
    client_presence_tracker: ClientPresenceTrackerDep,
    offline_status_manager: OfflineStatusManagerDep
) -> CommandSubmissionToTargetResponse:
    """
    Submit command to a specific target client within a session
    
    Core functionality for US-006: Targeted Client Command Submission  
    Enhanced with US-013: Non Existent Client Error Handling
    Enhanced with US-014: Offline Client Command Rejection
    - Command is queued for specific target client only
    - Only the target client will receive this command during polling
    - FIFO queue management ensures fair command processing
    - Rejects commands targeting clients that have not registered via polling
    - Rejects commands targeting offline clients to prevent command loss
    
    Args:
        session_id: The session identifier where the command will be submitted
        command_request: Command details including content and target client
        session_repo: Session repository for data persistence
        command_validator: Command validation service
        command_queue_manager: Command queue management service
        client_presence_tracker: Client presence tracking service
        offline_status_manager: Offline status management service
        
    Returns:
        CommandSubmissionToTargetResponse: Command submission confirmation with details
        
    Raises:
        HTTPException: 404 Not Found when target client has not registered (US-013)
        HTTPException: 422 Unprocessable Entity when target client is offline (US-014)
    """
    # US-013: Non Existent Client Error Handling
    # Check if target client has ever registered (via polling) in this session
    client_presence = client_presence_tracker.get_client_presence(
        client_id=command_request.target_client_id,
        session_id=session_id
    )
    
    if client_presence is None:
        # US-013: Client has never registered via polling - reject command submission
        raise HTTPException(
            status_code=404,
            detail=f"Client '{command_request.target_client_id}' has not registered in session '{session_id}'. "
                   f"Clients must perform at least one polling request before receiving commands."
        )
    
    # US-014: Offline Client Command Rejection
    # Check if target client is currently online and eligible for commands
    if not offline_status_manager.is_client_eligible_for_commands(
        client_id=command_request.target_client_id,
        session_id=session_id
    ):
        # US-014: Client is offline - reject command submission to prevent command loss
        raise HTTPException(
            status_code=422,
            detail=f"Cannot submit command to offline client '{command_request.target_client_id}'. "
                   f"Client must be online to receive commands. Commands are rejected to prevent command loss."
        )
    
    # US-006: Original implementation continues for registered and online clients
    # Submit command to target client's queue using queue manager
    command = command_queue_manager.submit_command_to_target_client(
        session_id=session_id,
        target_client_id=command_request.target_client_id,
        command_content=command_request.command_content
    )
    
    # Return response with command information
    return CommandSubmissionToTargetResponse(
        command_id=command.command_id,
        execution_status=CommandExecutionStatus.PENDING,
        submission_timestamp=datetime.now(),
        target_client_id=command_request.target_client_id,
        estimated_completion_time=None  # Will be estimated after queue processing
    )