"""
Execution Result Manager Service

Manages unified result storage and query for all commands with automatic timeout handling.
Implementation of US-021: Unified Result Query Mechanism.
"""

from typing import Optional, Dict
from datetime import datetime

from public_tunnel.models.execution_result import (
    ExecutionResult, 
    ExecutionResultStatus,
    UnifiedResultQueryResponse
)


class InMemoryExecutionResultManager:
    """In-memory implementation of execution result management
    
    Provides unified storage and query for all command results.
    Results are indexed by command_id for consistent access.
    """
    
    def __init__(self):
        # Command-id indexed storage for unified results
        self._results: Dict[str, ExecutionResult] = {}
    
    def store_result(self, result: ExecutionResult) -> None:
        """Store execution result with command-id indexing
        
        Args:
            result: ExecutionResult to store
        """
        self._results[result.command_id] = result
    
    def get_result_by_command_id(self, command_id: str) -> Optional[ExecutionResult]:
        """Get execution result by command_id
        
        Args:
            command_id: Command identifier to query
            
        Returns:
            ExecutionResult if found, None otherwise
        """
        return self._results.get(command_id)
    
    def create_and_store_result(
        self,
        command_id: str,
        session_id: str,
        client_id: str,
        execution_status: ExecutionResultStatus = ExecutionResultStatus.PENDING,
        result_content: Optional[str] = None,
        error_message: Optional[str] = None
    ) -> ExecutionResult:
        """Create and store new execution result
        
        Args:
            command_id: Command identifier for indexing
            session_id: Session identifier
            client_id: Client identifier
            execution_status: Current execution status
            result_content: Execution result content (optional)
            error_message: Error message if failed (optional)
            
        Returns:
            Created ExecutionResult instance
        """
        result = ExecutionResult(
            command_id=command_id,
            execution_status=execution_status,
            client_id=client_id,
            session_id=session_id
        )
        
        if result_content:
            result.result_content = result_content
            
        if error_message:
            result.error_message = error_message
            
        self.store_result(result)
        return result
    
    def update_result_status(
        self, 
        command_id: str,
        new_status: ExecutionResultStatus,
        result_content: Optional[str] = None,
        error_message: Optional[str] = None
    ) -> bool:
        """Update execution result status
        
        Args:
            command_id: Command identifier to update
            new_status: New execution status
            result_content: Updated result content (optional)
            error_message: Updated error message (optional)
            
        Returns:
            True if update successful, False if result not found
        """
        result = self._results.get(command_id)
        if not result:
            return False
        
        result.execution_status = new_status
        
        if new_status == ExecutionResultStatus.RUNNING and not result.started_at:
            result.started_at = datetime.now()
        elif new_status in [ExecutionResultStatus.COMPLETED, ExecutionResultStatus.FAILED]:
            result.completed_at = datetime.now()
            
        if result_content is not None:
            result.result_content = result_content
            
        if error_message is not None:
            result.error_message = error_message
            
        return True
    
    def get_unified_response(self, command_id: str) -> Optional[UnifiedResultQueryResponse]:
        """Get unified result response for command
        
        Args:
            command_id: Command identifier to query
            
        Returns:
            UnifiedResultQueryResponse if found, None otherwise
        """
        result = self._results.get(command_id)
        if not result:
            return None
        
        return result.to_unified_response()
    
    def clear_all_results(self) -> None:
        """Clear all stored results (for testing)"""
        self._results.clear()