from conftest import BDDPhase
from datetime import datetime, timedelta

def execute(context):
    """Verify that client's last_seen timestamp was updated"""
    context.phase = BDDPhase.THEN
    
    # Verify polling was successful
    assert context.polling_response.status_code == 200, \
        f"Polling should succeed, got {context.polling_response.status_code}"
    
    # Query the client's presence status to verify timestamp update
    presence_response = context.test_client.get(
        f"/api/sessions/{context.expected_session_id}/clients/{context.client_id}/presence"
    )
    
    # Presence tracking is now implemented, should return 200
    assert presence_response.status_code == 200, \
        f"Presence query should return 200, got {presence_response.status_code}"
    
    if presence_response.status_code == 200:
        presence_data = presence_response.json()
        
        # Verify last_seen timestamp is recent (within last few seconds)
        last_seen_str = presence_data.get("last_seen_timestamp")
        assert last_seen_str is not None, "last_seen_timestamp should be present"
        
        last_seen = datetime.fromisoformat(last_seen_str.replace("Z", "+00:00"))
        now = datetime.now()
        time_diff = abs((now - last_seen).total_seconds())
        
        assert time_diff < 60, f"last_seen timestamp should be recent, but was {time_diff} seconds ago"