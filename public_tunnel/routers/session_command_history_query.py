"""
US-019: Session Command History Query Router

Handles command history queries from specific sessions.
Allows AI assistant to list and review past command operations.
"""

from fastapi import APIRouter, HTTPException
from public_tunnel.models.session import SessionCommandHistoryResponse
from public_tunnel.dependencies.providers import SessionRepositoryDep, ExecutionResultManagerDep

router = APIRouter(tags=["session-command-history"])


@router.get("/api/sessions/{session_id}/commands/history", response_model=SessionCommandHistoryResponse)
async def get_session_command_history(
    session_id: str,
    session_repo: SessionRepositoryDep,
    result_manager: ExecutionResultManagerDep
) -> SessionCommandHistoryResponse:
    """
    Get command history for a specific session
    
    US-019 Implementation: allows AI assistant to list command history in a session
    so that it can review past operations and query details for each command.
    
    Args:
        session_id: The session identifier to query command history for
        session_repo: Session repository for data retrieval
        result_manager: Execution result manager for command history
        
    Returns:
        SessionCommandHistoryResponse: List of command IDs and session information
        
    Raises:
        HTTPException: 501 Not Implemented during API skeleton phase
    """
    # Get all command IDs that have been executed in this session
    command_ids = result_manager.get_command_ids_by_session(session_id)
    
    return SessionCommandHistoryResponse(
        session_id=session_id,
        command_ids=command_ids,
        total_commands=len(command_ids)
    )