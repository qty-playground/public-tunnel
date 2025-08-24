"""
US-009: Client Single Command Retrieval Router

Provides a client-focused API for retrieving single commands with execution pace control.
This is the client-centric implementation of single command polling.
"""

from fastapi import APIRouter, HTTPException

from public_tunnel.models.command import ClientCommandRetrievalResponse
from public_tunnel.dependencies.providers import CommandQueueManagerDep
from public_tunnel.models.command import Command

router = APIRouter(tags=["client-single-command-retrieval"])


def build_command_response_data(command: Command) -> dict:
    """
    Build command data dictionary for client response
    
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
    "/api/sessions/{session_id}/clients/{client_id}/command",
    response_model=ClientCommandRetrievalResponse,
    summary="Client retrieves single command to control execution pace",
    description="US-009: Returns single command for client, optimized for execution pace control. Command is removed from queue on retrieval."
)
async def retrieve_single_command_for_execution_control(
    session_id: str,
    client_id: str,
    queue_manager: CommandQueueManagerDep
) -> ClientCommandRetrievalResponse:
    """
    Client retrieves single command to control execution pace.
    
    US-009 Implementation:
    - Client-focused API design for single command retrieval
    - Command is immediately removed from queue upon retrieval
    - Provides execution pace control through has_more_commands indicator
    - Simplified response format optimized for client consumption
    
    Args:
        session_id: Target session identifier
        client_id: Client identifier requesting command
        queue_manager: Command queue management service
        
    Returns:
        ClientCommandRetrievalResponse: Single command with execution pace control info
    """
    command, remaining_queue_size = queue_manager.get_next_command_with_queue_info(
        session_id=session_id,
        client_id=client_id
    )
    
    command_dict = build_command_response_data(command) if command else None
    
    return ClientCommandRetrievalResponse(
        session_id=session_id,
        client_id=client_id,
        command=command_dict,
        has_more_commands=remaining_queue_size > 0,
        queue_size=remaining_queue_size
    )