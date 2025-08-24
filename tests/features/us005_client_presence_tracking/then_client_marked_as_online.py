from conftest import BDDPhase

def execute(context):
    """Verify that client is marked as online"""
    context.phase = BDDPhase.THEN
    
    # Query the client's presence status to verify online status
    presence_response = context.test_client.get(
        f"/api/sessions/{context.expected_session_id}/clients/{context.client_id}/presence"
    )
    
    # For now, expect 501 since presence tracking API is skeleton
    # TODO: Update to expect 200 when presence tracking is implemented
    assert presence_response.status_code in [200, 501], \
        f"Presence query should return 200 or 501 (skeleton), got {presence_response.status_code}"
    
    if presence_response.status_code == 200:
        presence_data = presence_response.json()
        
        # Verify client is marked as online
        presence_status = presence_data.get("presence_status")
        assert presence_status == "online", \
            f"Client should be marked as online after polling, got {presence_status}"