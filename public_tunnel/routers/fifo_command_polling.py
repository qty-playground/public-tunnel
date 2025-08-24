"""
US-007: Command FIFO Queue Management Router

Handles FIFO-ordered command polling from specified sessions.
Ensures commands are returned in first-in-first-out order with single command per polling.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Dict, Any

from public_tunnel.models.session import FIFOCommandPollingResponse
from public_tunnel.dependencies.providers import CommandQueueManagerDep
from public_tunnel.models.command import Command

router = APIRouter(tags=["fifo-command-polling"])


def convert_command_to_response_format(command: Command) -> Dict[str, Any]:
    """
    Convert Command domain object to response dictionary format
    
    Args:
        command: Command domain object
        
    Returns:
        Dict containing command data in API response format
    """
    return {
        "command_id": command.command_id,
        "content": command.content,
        "target_client": command.target_client,
        "session_id": command.session_id
    }


@router.get(
    "/api/sessions/{session_id}/clients/{client_id}/commands/poll",
    response_model=FIFOCommandPollingResponse,
    summary="Client polls for commands in FIFO order from specified session",
    description="US-007: Returns single command in first-in-first-out order. Each polling returns only one command."
)
async def poll_commands_in_fifo_order_from_session(
    session_id: str,
    client_id: str,
    queue_manager: CommandQueueManagerDep
) -> FIFOCommandPollingResponse:
    """
    Client polls for commands from specified session in FIFO order.
    
    US-007 Implementation:
    - Commands are queued in FIFO order
    - Each polling returns only ONE command
    - Commands returned in first-in-first-out sequence
    - Queue position and size information provided
    
    Args:
        session_id: Target session identifier
        client_id: Client identifier requesting commands
        queue_manager: Command queue management service
        
    Returns:
        FIFOCommandPollingResponse: Single command in FIFO order with queue info
    """
    command, remaining_queue_size = queue_manager.get_next_command_with_queue_info(
        session_id=session_id,
        client_id=client_id
    )
    
    if command:
        command_dict = convert_command_to_response_format(command)
        
        return FIFOCommandPollingResponse(
            session_id=session_id,
            client_id=client_id,
            command=command_dict,
            queue_position=0,
            total_queue_size=remaining_queue_size
        )
    else:
        return FIFOCommandPollingResponse(
            session_id=session_id,
            client_id=client_id,
            command=None,
            queue_position=0,
            total_queue_size=0
        )