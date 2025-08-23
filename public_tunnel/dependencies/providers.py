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
        
    Note: Implementation will be added when Repository layer is implemented.
    """
    # TODO: return SessionRepository(connection_string=DATABASE_URL)
    pass


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
        
    Note: Implementation will be added when validation logic is needed.
    """
    # TODO: return CommandValidator()
    pass


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


# Type aliases for cleaner router signatures
SessionRepositoryDep = Annotated[object, Depends(get_session_repository)]
CommandRepositoryDep = Annotated[object, Depends(get_command_repository)]
ClientRepositoryDep = Annotated[object, Depends(get_client_repository)]
CommandValidatorDep = Annotated[object, Depends(get_command_validator)]
SessionManagerDep = Annotated[object, Depends(get_session_manager)]