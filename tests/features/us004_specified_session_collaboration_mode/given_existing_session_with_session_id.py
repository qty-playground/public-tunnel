from conftest import BDDPhase

def execute(context):
    """Set up an existing session with a specific session-id and add existing clients"""
    context.phase = BDDPhase.GIVEN
    
    # Set up test data - create a specific session-id  
    context.target_session_id = "collaboration-session-001"
    context.new_client_id = "test-client-004"
    context.existing_client_ids = ["existing-client-001", "existing-client-002"]
    
    # Register existing clients in the target session first
    # This ensures the session exists and has clients
    for client_id in context.existing_client_ids:
        # Make existing clients poll to register themselves in the session
        response = context.test_client.post(
            f"/api/sessions/{context.target_session_id}/poll",
            json={"client_id": client_id}
        )
        assert response.status_code == 200
        
    context.initial_client_count = len(context.existing_client_ids)