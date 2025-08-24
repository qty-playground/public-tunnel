"""
Command Queue Manager Service for US-006: Targeted Client Command Submission

Manages FIFO queues for each target client within sessions.
Ensures commands are delivered only to their intended recipients.
"""

from typing import Dict, List, Optional, Set
from collections import deque
from datetime import datetime
from public_tunnel.models.command import Command
import threading


class CommandQueueManager:
    """
    Manages command queues for targeted client command submission
    
    Features:
    - FIFO queues per client per session
    - Thread-safe operations
    - Command queue isolation
    """
    
    def __init__(self):
        """Initialize empty command queue manager"""
        # Structure: {session_id: {client_id: deque[Command]}}
        self._command_queues: Dict[str, Dict[str, deque]] = {}
        self._lock = threading.RLock()
    
    def submit_command_to_target_client(
        self, 
        session_id: str, 
        target_client_id: str, 
        command_content: str
    ) -> Command:
        """
        Submit command to specific target client queue
        
        Args:
            session_id: Session identifier
            target_client_id: Target client identifier  
            command_content: Command content to execute
            
        Returns:
            Command: Created command object with unique ID
        """
        with self._lock:
            # Ensure session exists
            if session_id not in self._command_queues:
                self._command_queues[session_id] = {}
            
            # Ensure client queue exists
            if target_client_id not in self._command_queues[session_id]:
                self._command_queues[session_id][target_client_id] = deque()
            
            # Create command with unique ID
            import uuid
            command_id = str(uuid.uuid4())
            command = Command(
                command_id=command_id,
                content=command_content,
                target_client=target_client_id,
                session_id=session_id
            )
            
            # Add to target client's queue (FIFO)
            self._command_queues[session_id][target_client_id].append(command)
            
            return command
    
    def get_next_command_for_client(
        self, 
        session_id: str, 
        client_id: str
    ) -> Optional[Command]:
        """
        Get next command for specific client (FIFO)
        
        Args:
            session_id: Session identifier
            client_id: Client identifier requesting commands
            
        Returns:
            Command: Next command for this client, or None if queue is empty
        """
        with self._lock:
            if session_id not in self._command_queues:
                return None
                
            if client_id not in self._command_queues[session_id]:
                return None
            
            client_queue = self._command_queues[session_id][client_id]
            if not client_queue:
                return None
                
            # Return and remove first command (FIFO)
            return client_queue.popleft()
    
    def get_queue_size_for_client(
        self, 
        session_id: str, 
        client_id: str
    ) -> int:
        """
        Get number of pending commands for specific client
        
        Args:
            session_id: Session identifier
            client_id: Client identifier
            
        Returns:
            int: Number of pending commands in client's queue
        """
        with self._lock:
            if session_id not in self._command_queues:
                return 0
                
            if client_id not in self._command_queues[session_id]:
                return 0
                
            return len(self._command_queues[session_id][client_id])
    
    def get_all_clients_with_commands_in_session(self, session_id: str) -> Set[str]:
        """
        Get all clients that have pending commands in session
        
        Args:
            session_id: Session identifier
            
        Returns:
            Set[str]: Set of client IDs with pending commands
        """
        with self._lock:
            if session_id not in self._command_queues:
                return set()
            
            clients_with_commands = set()
            for client_id, queue in self._command_queues[session_id].items():
                if queue:  # Non-empty queue
                    clients_with_commands.add(client_id)
            
            return clients_with_commands
    
    def clear_session_queues(self, session_id: str) -> None:
        """
        Clear all command queues for a session
        
        Args:
            session_id: Session identifier to clear
        """
        with self._lock:
            if session_id in self._command_queues:
                del self._command_queues[session_id]


class InMemoryCommandQueueManager(CommandQueueManager):
    """In-memory implementation of CommandQueueManager for development/testing"""
    pass