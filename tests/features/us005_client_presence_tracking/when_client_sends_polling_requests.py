from conftest import BDDPhase

def execute(context):
    """Simulate client sending polling requests to trigger presence tracking"""
    context.phase = BDDPhase.WHEN
    
    # Send polling request - this should trigger presence tracking (US-005)
    # Using the existing endpoint that should integrate presence tracking
    polling_response = context.test_client.get(
        f"/api/sessions/default/poll?client_id={context.client_id}"
    )
    
    # Store the response for verification (this is WHEN phase result collection)
    context.polling_response = polling_response