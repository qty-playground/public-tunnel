from conftest import BDDPhase

def execute(context):
    """Verify that the client has been marked as offline in the system"""
    context.phase = BDDPhase.THEN
    
    # Step 1: API level verification - check HTTP response from force offline check
    assert hasattr(context, 'force_check_response'), "force_check_response should be available from When step"
    
    # Verify force offline check API responded successfully
    assert context.force_check_response.status_code == 200, (
        f"Force offline check API failed with status {context.force_check_response.status_code}"
    )
    
    force_check_data = context.force_check_response.json()
    assert "checked_clients_count" in force_check_data
    assert "newly_offline_clients_count" in force_check_data
    assert force_check_data["checked_clients_count"] >= 1, "Should have checked at least 1 client"
    
    # Step 2: Query detailed offline status via API
    offline_status_response = context.test_client.get(
        f"/api/sessions/{context.session_id}/clients/offline-status"
    )
    
    # GREEN Stage 2: Detailed verification logic
    
    # API level verification - HTTP response should be successful
    assert offline_status_response.status_code == 200, (
        f"Offline status API failed with status {offline_status_response.status_code}"
    )
    
    offline_status_data = offline_status_response.json()
    assert isinstance(offline_status_data, list), "Response should be a list of client status info"
    
    # Find our test client in the response
    client_status = None
    for client_info in offline_status_data:
        if client_info["client_id"] == context.client_id:
            client_status = client_info
            break
    
    assert client_status is not None, f"Client {context.client_id} not found in offline status response"
    
    # State level verification - verify the client is marked as offline
    assert client_status["presence_status"] == "offline", (
        f"Client {context.client_id} should be marked as offline, "
        f"but status is {client_status['presence_status']}"
    )
    
    # Verify offline timestamp is present
    assert "last_seen_timestamp" in client_status
    assert "seconds_since_last_seen" in client_status
    assert client_status["seconds_since_last_seen"] is not None
    assert client_status["seconds_since_last_seen"] > 0
    
    # Verify threshold information
    assert "offline_threshold_seconds" in client_status
    assert client_status["offline_threshold_seconds"] > 0
    
    # Verify command eligibility - offline clients should not be eligible
    assert "is_eligible_for_commands" in client_status
    assert client_status["is_eligible_for_commands"] == False, (
        "Offline clients should not be eligible for commands"
    )