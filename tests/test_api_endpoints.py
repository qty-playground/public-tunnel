"""Example tests demonstrating FastAPI TestClient usage patterns"""

import pytest
from fastapi.testclient import TestClient


def test_root_endpoint_with_test_client_fixture(test_client: TestClient):
    """Test using standalone test_client fixture for simple endpoint testing"""
    response = test_client.get("/")
    
    assert response.status_code == 200
    assert response.json() == {"message": "Public Tunnel API is running"}


def test_health_endpoint_with_test_client_fixture(test_client: TestClient):
    """Test health endpoint using standalone test_client fixture"""
    response = test_client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root_endpoint_with_bdd_context(context):
    """Test using BDD ScenarioContext for structured testing"""
    # GIVEN: We have an API client
    context.phase = context.phase  # Already in GIVEN phase
    
    # WHEN: We call the root endpoint
    from conftest import BDDPhase
    context.phase = BDDPhase.WHEN
    context.response = context.test_client.get("/")
    
    # THEN: We get the expected response
    context.phase = BDDPhase.THEN
    assert context.response.status_code == 200
    assert context.response.json() == {"message": "Public Tunnel API is running"}


def test_health_endpoint_with_bdd_context(context):
    """Test health endpoint using BDD ScenarioContext"""
    from conftest import BDDPhase
    
    # GIVEN: Initial state (already in GIVEN phase)
    
    # WHEN: We call the health endpoint
    context.phase = BDDPhase.WHEN
    context.response = context.test_client.get("/health")
    
    # THEN: We verify the response
    context.phase = BDDPhase.THEN
    assert context.response.status_code == 200
    assert context.response.json() == {"status": "healthy"}


def test_nonexistent_endpoint(test_client: TestClient):
    """Test that non-existent endpoints return 404"""
    response = test_client.get("/nonexistent")
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_async_compatible_endpoint(test_client: TestClient):
    """Example showing async test compatibility"""
    # The TestClient handles async endpoints automatically
    response = test_client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_bdd_phase_enforcement(context):
    """Test that BDD phase enforcement works correctly"""
    from conftest import BDDPhase
    
    # GIVEN: Set up test data
    context.test_data = "initial_value"
    
    # WHEN: Perform action and collect results
    context.phase = BDDPhase.WHEN
    context.result = "action_result"
    
    # Verify we cannot modify input state in WHEN phase
    with pytest.raises(AttributeError, match="Cannot modify input state.*in WHEN phase"):
        context.test_data = "modified_value"
    
    # THEN: Verify results (read-only phase)
    context.phase = BDDPhase.THEN
    assert context.test_data == "initial_value"
    assert context.result == "action_result"
    
    # Verify we cannot set attributes in THEN phase
    with pytest.raises(AttributeError, match="Cannot set attribute.*in THEN phase"):
        context.verification = "should_fail"


def test_context_state_methods(context):
    """Test ScenarioContext utility methods"""
    from conftest import BDDPhase
    
    # GIVEN: Set up initial state
    context.input1 = "value1"
    context.input2 = "value2"
    
    # Verify input state tracking
    input_state = context.get_input_state()
    assert input_state == {"input1": "value1", "input2": "value2"}
    
    # WHEN: Collect results
    context.phase = BDDPhase.WHEN
    context.result1 = "output1"
    context.result2 = "output2"
    
    # Verify results tracking
    results = context.get_results()
    assert results == {"result1": "output1", "result2": "output2"}
    
    # THEN: Verify state separation
    context.phase = BDDPhase.THEN
    assert context.get_input_state() == {"input1": "value1", "input2": "value2"}
    assert context.get_results() == {"result1": "output1", "result2": "output2"}