"""
Centralized dependency injection providers for Public Tunnel application.

This unified approach ensures:
- Consistent service instances across all routers
- Easy testing with single point of override in conftest.py
- Clear dependency visibility and management
- Proper separation of concerns

Usage pattern:
1. Define provider functions here
2. Import in routers and use with Depends()
3. Override in conftest.py for testing

Example:
    # In router:
    from public_tunnel.dependencies.providers import get_session_repository
    
    @router.post("/sessions")
    async def create_session(
        session_repo: Annotated[SessionRepository, Depends(get_session_repository)]
    ):
        pass
        
    # In conftest.py:
    app.dependency_overrides[get_session_repository] = get_test_session_repository
"""

from typing import Annotated
from fastapi import Depends


# Repository Providers (for external data exchange)
def get_session_repository():
    """Provide unified Session Repository instance
    
    Returns the same SessionRepository instance across all routers.
    Can be easily overridden in conftest.py for testing.
    
    Returns:
        SessionRepository: Session data repository instance
    """
    from public_tunnel.repositories.session_repository import InMemorySessionRepository
    
    # Global singleton instance for development/testing
    if not hasattr(get_session_repository, '_instance'):
        get_session_repository._instance = InMemorySessionRepository()
    
    return get_session_repository._instance


def get_command_repository():
    """Provide unified Command Repository instance
    
    Returns the same CommandRepository instance across all routers.
    Can be easily overridden in conftest.py for testing.
    
    Returns:
        CommandRepository: Command data repository instance
        
    Note: Implementation will be added when Repository layer is implemented.
    """
    # TODO: return CommandRepository(connection_string=DATABASE_URL)  
    pass


def get_client_repository():
    """Provide unified Client Repository instance
    
    Returns the same ClientRepository instance across all routers.
    Can be easily overridden in conftest.py for testing.
    
    Returns:
        ClientRepository: Client data repository instance
        
    Note: Implementation will be added when Repository layer is implemented.
    """
    # TODO: return ClientRepository(connection_string=DATABASE_URL)
    pass


# Service Providers (for business logic services)
def get_command_validator():
    """Provide unified Command Validator service
    
    Returns the same CommandValidator instance across all routers.
    Can be easily overridden in conftest.py for testing.
    
    Returns:
        CommandValidator: Command validation service instance
        
    Note: US-006 implementation - validates command submissions
    """
    # CommandValidator implementation for US-006 - currently not needed
    # Basic command validation is handled at API level via Pydantic models
    pass


def get_command_queue_manager():
    """Provide unified Command Queue Manager service
    
    Returns the same CommandQueueManager instance across all routers.
    Manages FIFO queues for each target client within sessions.
    
    Returns:
        CommandQueueManager: Command queue management service instance
        
    Note: US-006 implementation - manages targeted command queues
    """
    from public_tunnel.services.command_queue_manager import InMemoryCommandQueueManager
    
    # Global singleton instance for development/testing
    if not hasattr(get_command_queue_manager, '_instance'):
        get_command_queue_manager._instance = InMemoryCommandQueueManager()
    
    return get_command_queue_manager._instance


def get_session_manager():
    """Provide unified Session Manager service
    
    Returns the same SessionManager instance across all routers.
    Can be easily overridden in conftest.py for testing.
    
    Returns:
        SessionManager: Session management service instance
        
    Note: Implementation will be added when session logic is needed.
    """
    # TODO: return SessionManager()
    pass


def get_client_presence_tracker():
    """Provide unified Client Presence Tracker service
    
    Returns the same ClientPresenceTracker instance across all routers.
    Can be easily overridden in conftest.py for testing.
    
    Returns:
        ClientPresenceTracker: Client presence tracking service instance
    """
    from public_tunnel.services.client_presence_tracker import InMemoryClientPresenceTracker
    
    # Global singleton instance for development/testing
    if not hasattr(get_client_presence_tracker, '_instance'):
        get_client_presence_tracker._instance = InMemoryClientPresenceTracker(
            offline_threshold_seconds=60  # 1 minute threshold
        )
    
    return get_client_presence_tracker._instance


def get_offline_status_manager():
    """Provide unified Offline Status Manager service
    
    Returns the same OfflineStatusManager instance across all routers.
    Can be easily overridden in conftest.py for testing.
    
    Returns:
        OfflineStatusManager: Offline status management service instance
        
    Note: US-016 implementation - manages offline status operations
    """
    from public_tunnel.services.offline_status_manager import OfflineStatusManager
    
    # Global singleton instance for development/testing
    if not hasattr(get_offline_status_manager, '_instance'):
        # Get the shared presence tracker instance
        presence_tracker = get_client_presence_tracker()
        get_offline_status_manager._instance = OfflineStatusManager(presence_tracker)
    
    return get_offline_status_manager._instance


def get_execution_result_manager():
    """Provide unified Execution Result Manager service
    
    Returns the same ExecutionResultManager instance across all routers.
    Can be easily overridden in conftest.py for testing.
    
    Returns:
        ExecutionResultManager: Execution result management service instance
        
    Note: US-021 implementation - manages unified result storage and query
    """
    from public_tunnel.services.execution_result_manager import InMemoryExecutionResultManager
    
    # Global singleton instance for development/testing
    if not hasattr(get_execution_result_manager, '_instance'):
        get_execution_result_manager._instance = InMemoryExecutionResultManager()
    
    return get_execution_result_manager._instance


def get_file_manager():
    """Provide unified File Manager service
    
    Returns the same FileManager instance across all routers.
    Can be easily overridden in conftest.py for testing.
    
    Returns:
        FileManager: File management service instance
        
    Note: US-010 implementation - manages file upload, download, and session-based storage
    """
    from public_tunnel.services.file_manager import InMemoryFileManager
    
    # Global singleton instance for development/testing
    if not hasattr(get_file_manager, '_instance'):
        get_file_manager._instance = InMemoryFileManager()
    
    return get_file_manager._instance


def get_session_file_access_validator():
    """Provide unified Session File Access Validator service
    
    Returns the same SessionFileAccessValidator instance across all routers.
    Can be easily overridden in conftest.py for testing.
    
    Returns:
        SessionFileAccessValidator: Session file access validation service instance
        
    Note: US-012 implementation - validates file access permissions across sessions
    """
    from public_tunnel.services.session_file_access_validator import InMemorySessionFileAccessValidator
    
    # Global singleton instance for development/testing
    if not hasattr(get_session_file_access_validator, '_instance'):
        # Get the file manager instance for file ownership validation
        file_manager = get_file_manager()
        get_session_file_access_validator._instance = InMemorySessionFileAccessValidator(file_manager)
    
    return get_session_file_access_validator._instance


# Type aliases for cleaner router signatures
SessionRepositoryDep = Annotated[object, Depends(get_session_repository)]
CommandRepositoryDep = Annotated[object, Depends(get_command_repository)]
ClientRepositoryDep = Annotated[object, Depends(get_client_repository)]
CommandValidatorDep = Annotated[object, Depends(get_command_validator)]
CommandQueueManagerDep = Annotated[object, Depends(get_command_queue_manager)]
SessionManagerDep = Annotated[object, Depends(get_session_manager)]
ClientPresenceTrackerDep = Annotated[object, Depends(get_client_presence_tracker)]
OfflineStatusManagerDep = Annotated[object, Depends(get_offline_status_manager)]
ExecutionResultManagerDep = Annotated[object, Depends(get_execution_result_manager)]
FileManagerDep = Annotated[object, Depends(get_file_manager)]
SessionFileAccessValidatorDep = Annotated['InMemorySessionFileAccessValidator', Depends(get_session_file_access_validator)]