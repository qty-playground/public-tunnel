"""
Command submission router for submitting commands to specific clients.

Handles command submission functionality for testing US-016: Client Offline Status Management
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from public_tunnel.dependencies.providers import OfflineStatusManagerDep
import uuid

router = APIRouter(tags=["command-submission"])


class CommandSubmissionRequest(BaseModel):
    """Request model for command submission"""
    command: str
    target_client: str


class CommandSubmissionResponse(BaseModel):
    """Response model for command submission"""
    command_id: str
    status: str
    message: str


@router.post("/api/sessions/{session_id}/commands", response_model=CommandSubmissionResponse)
async def submit_command_to_client(
    session_id: str,
    request: CommandSubmissionRequest,
    offline_status_manager: OfflineStatusManagerDep
) -> CommandSubmissionResponse:
    """
    Submit command to a specific client in a session
    
    This endpoint implements US-016: offline clients cannot receive new commands.
    Commands are rejected if the target client is offline.
    """
    # GREEN Stage 2: Real implementation with offline status checking
    
    # Check if target client is eligible for commands (i.e., online)
    is_eligible = offline_status_manager.is_client_eligible_for_commands(
        request.target_client, 
        session_id
    )
    
    if not is_eligible:
        # US-016: Reject command submission to offline clients
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Cannot submit command to offline client '{request.target_client}'. "
                   f"Client must be online to receive commands."
        )
    
    # If client is online, accept the command (simplified implementation)
    command_id = str(uuid.uuid4())
    
    return CommandSubmissionResponse(
        command_id=command_id,
        status="queued",
        message=f"Command successfully queued for client '{request.target_client}'"
    )