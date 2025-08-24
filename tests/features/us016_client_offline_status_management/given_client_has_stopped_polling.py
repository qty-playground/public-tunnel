from conftest import BDDPhase
from datetime import datetime, timedelta

def execute(context):
    """Set up a client that was previously polling but has now stopped"""
    context.phase = BDDPhase.GIVEN
    
    # Set up test data for a client that will stop polling
    context.client_id = "test-client-offline-001"
    context.session_id = "default"  # US-003: clients join default session
    context.offline_threshold_seconds = 2  # Use very short threshold for testing (2 seconds)
    
    # Step 1: Configure the system to use a short offline threshold for testing
    threshold_config_response = context.test_client.put(
        "/api/configuration/offline-threshold",
        json={"offline_threshold_seconds": context.offline_threshold_seconds}
    )
    assert threshold_config_response.status_code == 200, (
        f"Failed to configure offline threshold: {threshold_config_response.status_code}"
    )
    
    # Step 2: Client sends initial polling request to establish presence
    # Using API approach to simulate real user behavior
    polling_response = context.test_client.get(
        f"/api/sessions/default/poll?client_id={context.client_id}"
    )
    
    # Verify the client was registered successfully
    assert polling_response.status_code == 200
    polling_data = polling_response.json()
    assert polling_data["client_id"] == context.client_id
    assert polling_data["session_id"] == "default"
    
    # Store the initial polling timestamp for reference
    context.initial_polling_time = datetime.now()
    
    # Step 3: Simulate the client stopping polling
    # The key point is that we don't send any more polling requests
    # This creates the scenario where the client "has stopped polling"