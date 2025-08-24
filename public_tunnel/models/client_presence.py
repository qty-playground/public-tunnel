"""
Client presence tracking models for public tunnel API

Contains Pydantic models related to client presence and status management.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class ClientPresenceStatus(str, Enum):
    """Client presence status enumeration"""
    ONLINE = "online"
    OFFLINE = "offline"
    UNKNOWN = "unknown"


class ClientPresenceInfo(BaseModel):
    """Information about client presence status"""
    client_id: str = Field(description="Unique identifier for the client")
    session_id: str = Field(description="Session ID the client belongs to")
    presence_status: ClientPresenceStatus = Field(description="Current presence status")
    last_seen_timestamp: Optional[datetime] = Field(
        default=None,
        description="Last time the client was seen (via polling)"
    )
    first_seen_timestamp: Optional[datetime] = Field(
        default=None, 
        description="First time the client was registered"
    )
    heartbeat_interval_seconds: Optional[int] = Field(
        default=30,
        description="Expected heartbeat interval in seconds"
    )


class UpdateClientPresenceRequest(BaseModel):
    """Request to update client presence information"""
    client_id: str = Field(description="Unique identifier for the client")
    last_seen_timestamp: datetime = Field(description="Timestamp when client was last seen")


class UpdateClientPresenceResponse(BaseModel):
    """Response after updating client presence"""
    client_id: str = Field(description="Client ID that was updated")
    session_id: str = Field(description="Session ID the client belongs to") 
    previous_status: ClientPresenceStatus = Field(description="Previous presence status")
    current_status: ClientPresenceStatus = Field(description="Updated presence status")
    last_seen_timestamp: datetime = Field(description="Updated last seen timestamp")
    updated_at: datetime = Field(description="When this update occurred")


class ClientPresenceQueryResponse(BaseModel):
    """Response for querying client presence information"""
    client_id: str = Field(description="Client ID being queried")
    session_id: str = Field(description="Session ID the client belongs to")
    presence_status: ClientPresenceStatus = Field(description="Current presence status")
    last_seen_timestamp: Optional[datetime] = Field(
        default=None,
        description="Last time the client was seen"
    )
    online_duration_seconds: Optional[int] = Field(
        default=None,
        description="How long client has been online in seconds"
    )