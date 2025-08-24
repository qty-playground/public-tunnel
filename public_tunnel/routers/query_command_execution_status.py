"""
Query command execution status - Supporting US-006

Handles command execution status queries for targeted commands.
Supports the query functionality needed for US-006 command submission workflow.
"""

from fastapi import APIRouter, HTTPException
from public_tunnel.models.command import CommandExecutionStatusResponse
from public_tunnel.dependencies.providers import SessionRepositoryDep

router: APIRouter = APIRouter(tags=["command-status-query"])


@router.get("/api/sessions/{session_id}/commands/{command_id}/status", response_model=CommandExecutionStatusResponse)
async def get_command_execution_status_from_session(
    session_id: str, 
    command_id: str,
    session_repo: SessionRepositoryDep
) -> CommandExecutionStatusResponse:
    """
    Get execution status of a specific command within a session
    
    Supporting functionality for US-006: allows AI assistant to track 
    the execution status of commands submitted to target clients.
    
    Args:
        session_id: The session identifier where the command was submitted
        command_id: The unique command identifier to query
        session_repo: Session repository for data retrieval
        
    Returns:
        CommandExecutionStatusResponse: Current command execution status and details
        
    Raises:
        HTTPException: 501 Not Implemented during API skeleton phase
    """
    # API Skeleton Phase: Return 501 to indicate endpoint structure is ready
    # but business logic implementation is pending
    raise HTTPException(
        status_code=501,
        detail="Command execution status query not implemented yet"
    )