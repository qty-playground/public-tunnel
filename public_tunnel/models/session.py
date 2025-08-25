"""
Session models for public tunnel API

Contains Pydantic models related to session management and client registration.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ClientPollingRequest(BaseModel):
    """Request model for client polling to get commands"""
    client_id: str = Field(description="Unique identifier for the client")
    last_seen: Optional[datetime] = Field(
        default=None,
        description="Last seen timestamp for presence tracking"
    )
    

class ClientPollingResponse(BaseModel):
    """Response model for client polling request"""
    session_id: str = Field(description="Session ID the client is assigned to")
    client_id: str = Field(description="Client ID that was registered")
    commands: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="List of commands available for this client"
    )
    registration_status: str = Field(description="Registration status (new/existing)")


class SessionInfo(BaseModel):
    """Information about a session"""
    session_id: str = Field(description="Unique session identifier")
    client_count: int = Field(description="Number of clients in this session")
    created_at: datetime = Field(description="When the session was created")
    default_session: bool = Field(
        default=False,
        description="Whether this is the default session"
    )


class ClientRegistrationResponse(BaseModel):
    """Response when client is registered to a session"""
    session_id: str = Field(description="Session ID the client was assigned to")
    client_id: str = Field(description="Client ID that was registered")
    registration_timestamp: datetime = Field(description="When registration occurred")
    message: str = Field(description="Registration confirmation message")


class FIFOCommandPollingResponse(BaseModel):
    """US-007: Response model for FIFO command polling from specified session"""
    session_id: str = Field(description="Session ID where client is polling")
    client_id: str = Field(description="Client ID performing the polling")
    command: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Single command returned in FIFO order (None if no commands)"
    )
    queue_position: int = Field(
        description="Position in queue after this command (0 means no more commands)"
    )
    total_queue_size: int = Field(
        description="Total number of commands remaining in queue for this client"
    )


class SessionCommandHistoryResponse(BaseModel):
    """US-019: Response model for session command history query"""
    session_id: str = Field(description="Session ID being queried")
    command_ids: List[str] = Field(
        description="List of command IDs that have been executed in this session"
    )
    total_commands: int = Field(
        description="Total number of commands in the session history"
    )


class AdminSessionListResponse(BaseModel):
    """US-001: Response model for admin session list query"""
    sessions: List[SessionInfo] = Field(
        description="List of all sessions in the system"
    )
    total_sessions: int = Field(
        description="Total number of sessions"
    )
    queried_at: datetime = Field(
        description="Timestamp when the query was performed"
    )