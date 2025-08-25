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
    SessionManagerDep,
    ClientPresenceTrackerDep
)


router = APIRouter(tags=["client-polling"])


@router.get(
    "/api/sessions/default/poll",
    response_model=ClientPollingResponse,
    summary="Client polls for commands in default session",
    description="US-003: Allows client to automatically join default session and poll for commands. US-005: Updates client presence tracking."
)
async def poll_commands_from_default_session(
    client_id: str = Query(description="Unique client identifier"),
    session_repo: SessionRepositoryDep = None,
    client_repo: ClientRepositoryDep = None,
    session_manager: SessionManagerDep = None,
    presence_tracker: ClientPresenceTrackerDep = None
) -> ClientPollingResponse:
    """
    Client polls for commands from default session.
    
    This endpoint implements:
    - US-003: Default Session Auto Join - Client automatically joins default session
    - US-005: Client Presence Tracking - Updates client's last_seen timestamp
    
    Implementation:
    - Client automatically joins default session on first polling
    - Client ID is recorded in the session
    - Client's presence status is updated (last_seen timestamp)
    - Returns any pending commands for the client
    """
    # GREEN Stage 2: Real implementation for US-003
    default_session_id = session_repo.get_default_session_id()
    
    # Check if client is already in session
    is_existing_client = session_repo.is_client_in_session(default_session_id, client_id)
    
    # Add client to default session (idempotent operation)
    is_new_registration = session_repo.add_client_to_session(default_session_id, client_id)
    
    # US-005: Update client presence tracking
    if presence_tracker:
        presence_tracker.update_client_last_seen(client_id, default_session_id, datetime.now())
    
    # Determine registration status based on whether this is first time
    registration_status = "new" if is_new_registration else "existing"
    
    return ClientPollingResponse(
        session_id=default_session_id,
        client_id=client_id,
        commands=[],  # No commands implementation yet - will be added in later user stories
        registration_status=registration_status
    )


@router.post(
    "/api/sessions/{session_id}/poll",
    response_model=ClientPollingResponse,
    summary="Client polls for commands in specified session",
    description="US-004: Allows client to join existing session by specifying session-id and poll for commands. US-005: Updates client presence tracking."
)
async def poll_commands_from_specified_session(
    session_id: str,
    request: ClientPollingRequest,
    session_repo: SessionRepositoryDep = None,
    client_repo: ClientRepositoryDep = None,
    session_manager: SessionManagerDep = None,
    presence_tracker: ClientPresenceTrackerDep = None
) -> ClientPollingResponse:
    """
    Client polls for commands from specified session.
    
    This endpoint implements:
    - US-004: Specified Session Collaboration Mode - Client joins existing session
    - US-005: Client Presence Tracking - Updates client's last_seen timestamp
    
    Implementation:
    - Client joins the specified session
    - Client ID is recorded in the session  
    - Client's presence status is updated (last_seen timestamp)
    - Returns any pending commands for the client
    """
    # US-004: Real implementation for specified session collaboration mode
    client_id = request.client_id
    
    # Check if client is already in session
    is_existing_client = session_repo.is_client_in_session(session_id, client_id)
    
    # Add client to specified session (idempotent operation)
    # This will create the session if it doesn't exist (collaboration mode)
    is_new_registration = session_repo.add_client_to_session(session_id, client_id)
    
    # US-005: Update client presence tracking
    if presence_tracker:
        presence_tracker.update_client_last_seen(client_id, session_id, datetime.now())
    
    # Determine registration status based on whether this is first time
    registration_status = "new" if is_new_registration else "existing"
    
    return ClientPollingResponse(
        session_id=session_id,
        client_id=client_id,
        commands=[],  # No commands implementation yet - will be added in later user stories
        registration_status=registration_status
    )