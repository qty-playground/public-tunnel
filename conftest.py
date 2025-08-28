"""Root conftest.py for pytest configuration and shared fixtures"""

import pytest
from enum import Enum
from typing import Any, Dict
from fastapi.testclient import TestClient


class BDDPhase(Enum):
    """BDD test phases with different state management permissions"""
    GIVEN = "given"  # Setup phase - can set input state
    WHEN = "when"    # Action phase - can collect results, cannot modify input state  
    THEN = "then"    # Assertion phase - read-only access


class ScenarioContext:
    """
    BDD Test Context with phase-aware state management
    
    Enforces proper separation of concerns across Given-When-Then phases:
    - GIVEN: Can set input state and test data
    - WHEN: Can collect execution results, cannot modify input state
    - THEN: Read-only access for assertions
    """
    
    def __init__(self):
        object.__setattr__(self, '_phase', BDDPhase.GIVEN)
        object.__setattr__(self, '_input_state', {})
        object.__setattr__(self, '_results', {})
        
        # Initialize shared test infrastructure
        self._init_test_client()
    
    def _init_test_client(self) -> None:
        """Initialize test client for this scenario"""
        from public_tunnel.main import app
        
        # Create test client
        test_client = TestClient(app)
        
        # Store in internal state (accessible to all steps)
        object.__setattr__(self, '_test_client', test_client)
    
    @property
    def test_client(self) -> TestClient:
        """Get shared test client for this scenario"""
        return self._test_client
    
    def register_client(self, client_id: str, session_id: str = "default") -> None:
        """
        Register a client by sending polling request (common pattern for many tests)
        
        This helper function encapsulates the common pattern of client registration
        that's needed in most BDD tests. It should only be called during GIVEN phase.
        
        Args:
            client_id: The client ID to register
            session_id: The session ID to register in (defaults to "default")
            
        Raises:
            AssertionError: If client registration fails
            AttributeError: If called outside GIVEN phase
        """
        if self._phase != BDDPhase.GIVEN:
            raise AttributeError("register_client() can only be called during GIVEN phase")
        
        # Register client through polling API (proper external API usage)
        poll_response = self.test_client.get(
            f"/api/sessions/{session_id}/poll",
            params={"client_id": client_id}
        )
        
        assert poll_response.status_code == 200, (
            f"Client registration failed for {client_id} in session {session_id}: "
            f"HTTP {poll_response.status_code}"
        )
    
    @property
    def phase(self) -> BDDPhase:
        """Get current BDD phase"""
        return self._phase
    
    @phase.setter
    def phase(self, phase: BDDPhase) -> None:
        """Set current BDD phase to control state management permissions"""
        current_phase = self._phase
        
        # Define phase hierarchy: GIVEN(0) → WHEN(1) → THEN(2)
        phase_hierarchy = {
            BDDPhase.GIVEN: 0,
            BDDPhase.WHEN: 1,
            BDDPhase.THEN: 2
        }
        
        current_level = phase_hierarchy[current_phase]
        new_level = phase_hierarchy[phase]
        
        # Only allow phase upgrades (same level or higher)
        if new_level < current_level:
            raise ValueError(
                f"Invalid phase transition: {current_phase.value} → {phase.value}. "
                f"BDD phases can only progress forward: GIVEN → WHEN → THEN."
            )
        
        object.__setattr__(self, '_phase', phase)
    
    def __setattr__(self, name: str, value: Any) -> None:
        """Override attribute setting to enforce phase-based permissions"""
        # Allow internal attributes
        if name.startswith('_'):
            object.__setattr__(self, name, value)
            return
        
        # Handle phase property separately
        if name == 'phase':
            type(self).phase.__set__(self, value)
            return
            
        current_phase = self._phase
        
        if current_phase == BDDPhase.GIVEN:
            # GIVEN: Can set any state (input data, test setup)
            self._input_state[name] = value
            object.__setattr__(self, name, value)
            
        elif current_phase == BDDPhase.WHEN:
            # WHEN: Can collect results, cannot modify input state
            if name in self._input_state:
                raise AttributeError(
                    f"Cannot modify input state '{name}' in WHEN phase."
                )
            # Allow result collection
            self._results[name] = value
            object.__setattr__(self, name, value)
            
        elif current_phase == BDDPhase.THEN:
            # THEN: Read-only phase
            raise AttributeError(
                f"Cannot set attribute '{name}' in THEN phase."
            )
    
    def __getattr__(self, name: str) -> Any:
        """Standard attribute access - no restrictions on reading"""
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
    def get_input_state(self) -> Dict[str, Any]:
        """Get all input state set during GIVEN phase"""
        return self._input_state.copy()
    
    def get_results(self) -> Dict[str, Any]:
        """Get all results collected during WHEN phase"""  
        return self._results.copy()
    
    def clear_state(self) -> None:
        """Clear all state - use with caution, mainly for testing"""
        object.__setattr__(self, '_input_state', {})
        object.__setattr__(self, '_results', {})
        # Clear dynamic attributes (skip built-in properties)
        attrs_to_remove = [attr for attr in dir(self) 
                          if not attr.startswith('_') 
                          and not callable(getattr(self, attr))
                          and attr != 'phase']  # Skip phase property
        for attr in attrs_to_remove:
            delattr(self, attr)
    
    def cleanup(self) -> None:
        """Clean up test infrastructure"""
        from public_tunnel.main import app
        app.dependency_overrides.clear()


@pytest.fixture
def context() -> ScenarioContext:
    """Provide fresh ScenarioContext instance for each test scenario"""
    ctx = ScenarioContext()
    yield ctx
    # Cleanup after test
    ctx.cleanup()


@pytest.fixture
def test_client() -> TestClient:
    """
    Provide a standalone TestClient for simple FastAPI testing without BDD context.
    
    This fixture is useful for:
    - Simple API endpoint testing
    - Integration tests that don't need BDD structure
    - Quick smoke tests
    
    Example usage:
        def test_health_endpoint(test_client):
            response = test_client.get("/health")
            assert response.status_code == 200
            assert response.json() == {"status": "healthy"}
    """
    from public_tunnel.main import app
    
    with TestClient(app) as client:
        yield client
    
    # Cleanup after test
    app.dependency_overrides.clear()