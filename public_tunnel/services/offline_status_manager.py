"""
Offline status manager service

Handles offline status management operations including threshold configuration,
forced status checks, and command eligibility determination for US-016.
"""

from typing import Optional, List, Tuple
from datetime import datetime
from public_tunnel.models.client_presence import (
    OfflineThresholdConfiguration,
    ForceOfflineStatusCheckResponse,
    ClientOfflineStatusInfo
)
from public_tunnel.services.client_presence_tracker import InMemoryClientPresenceTracker


class OfflineStatusManager:
    """
    Service for managing client offline status operations
    
    Coordinates between ClientPresenceTracker and higher-level offline status 
    management operations. Provides business logic layer for US-016 requirements.
    """
    
    def __init__(self, presence_tracker: InMemoryClientPresenceTracker):
        """
        Initialize offline status manager
        
        Args:
            presence_tracker: Client presence tracking service instance
        """
        self.presence_tracker = presence_tracker
    
    def get_current_threshold_configuration(self) -> OfflineThresholdConfiguration:
        """
        Get current offline threshold configuration
        
        Returns:
            Current threshold configuration from presence tracker
        """
        return self.presence_tracker.get_offline_threshold_configuration()
    
    def update_threshold_configuration(self, new_threshold_seconds: int) -> Tuple[int, int, int]:
        """
        Update offline threshold configuration
        
        Args:
            new_threshold_seconds: New threshold value in seconds
            
        Returns:
            Tuple of (previous_threshold, current_threshold, affected_sessions_count)
        """
        previous_threshold, affected_sessions_count = self.presence_tracker.update_offline_threshold(
            new_threshold_seconds
        )
        return previous_threshold, new_threshold_seconds, affected_sessions_count
    
    def execute_force_offline_check_for_session(
        self, 
        session_id: str
    ) -> ForceOfflineStatusCheckResponse:
        """
        Execute forced offline status check for a specific session
        
        Args:
            session_id: Session ID to check clients for
            
        Returns:
            Detailed response about the forced offline check results
        """
        checked_count, newly_offline_count, already_offline_count = (
            self.presence_tracker.force_offline_status_check_for_session(session_id)
        )
        
        return ForceOfflineStatusCheckResponse(
            checked_clients_count=checked_count,
            newly_offline_clients_count=newly_offline_count,
            already_offline_clients_count=already_offline_count,
            session_id=session_id,
            check_timestamp=datetime.now()
        )
    
    def execute_force_offline_check_for_all_sessions(self) -> ForceOfflineStatusCheckResponse:
        """
        Execute forced offline status check for all sessions
        
        Returns:
            Detailed response about the system-wide forced offline check results
        """
        checked_count, newly_offline_count, already_offline_count = (
            self.presence_tracker.force_offline_status_check_for_session(session_id=None)
        )
        
        return ForceOfflineStatusCheckResponse(
            checked_clients_count=checked_count,
            newly_offline_clients_count=newly_offline_count,
            already_offline_clients_count=already_offline_count,
            session_id=None,  # Indicates system-wide check
            check_timestamp=datetime.now()
        )
    
    def get_detailed_offline_status_for_session(self, session_id: str) -> List[ClientOfflineStatusInfo]:
        """
        Get detailed offline status information for all clients in a session
        
        Args:
            session_id: Session ID to get detailed status for
            
        Returns:
            List of detailed client offline status information
        """
        return self.presence_tracker.get_detailed_offline_status_for_session(session_id)
    
    def get_all_clients_detailed_offline_status(self) -> List[ClientOfflineStatusInfo]:
        """
        Get detailed offline status information for all clients across all sessions
        
        Returns:
            List of detailed client offline status information for all clients
        """
        return self.presence_tracker.get_all_clients_offline_status()
    
    def is_client_eligible_for_commands(self, client_id: str, session_id: str) -> bool:
        """
        Check if client is eligible to receive new commands
        
        Args:
            client_id: Client unique identifier
            session_id: Session the client belongs to
            
        Returns:
            True if client can receive commands (is online), False otherwise
            
        Note: This is the core business rule for US-016 - offline clients cannot receive commands
        """
        presence_info = self.presence_tracker.get_client_presence(client_id, session_id)
        
        if not presence_info:
            return False
        
        # US-016 business rule: only online clients can receive new commands
        from public_tunnel.models.client_presence import ClientPresenceStatus
        return presence_info.presence_status == ClientPresenceStatus.ONLINE