"""
Client polling router for default session auto-join functionality.

Handles client registration and command polling for US-003: Default Session Auto Join
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime

from public_tunnel.models.session import (
    ClientPollingRequest,
    ClientPollingResponse,
    ClientRegistrationResponse
)
from public_tunnel.dependencies.providers import (
    SessionRepositoryDep,
    ClientRepositoryDep,
    SessionManagerDep
)


router = APIRouter(tags=["client-polling"])


@router.get(
    "/api/sessions/default/poll",
    response_model=ClientPollingResponse,
    summary="Client polls for commands in default session",
    description="US-003: Allows client to automatically join default session and poll for commands"
)
async def poll_commands_from_default_session(
    client_id: str = Query(description="Unique client identifier"),
    session_repo: SessionRepositoryDep = None,
    client_repo: ClientRepositoryDep = None,
    session_manager: SessionManagerDep = None
) -> ClientPollingResponse:
    """
    Client polls for commands from default session.
    
    This endpoint implements US-003: Default Session Auto Join
    - Client automatically joins default session on first polling
    - Client ID is recorded in the session
    - Returns any pending commands for the client
    """
    # GREEN Stage 2: Real implementation
    default_session_id = session_repo.get_default_session_id()
    
    # Check if client is already in session
    is_existing_client = session_repo.is_client_in_session(default_session_id, client_id)
    
    # Add client to default session (idempotent operation)
    is_new_registration = session_repo.add_client_to_session(default_session_id, client_id)
    
    # Determine registration status based on whether this is first time
    registration_status = "new" if is_new_registration else "existing"
    
    return ClientPollingResponse(
        session_id=default_session_id,
        client_id=client_id,
        commands=[],  # No commands implementation yet - will be added in later user stories
        registration_status=registration_status
    )


# NOTE: poll_commands_from_specified_session will be implemented in US-004
# US-003 only requires default session auto-join functionality