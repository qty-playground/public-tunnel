from conftest import BDDPhase

def execute(context):
    """Set up a client that will poll regularly for presence tracking"""
    context.phase = BDDPhase.GIVEN
    
    # Set up test data for a regular polling client
    context.client_id = "test-client-presence-001"
    context.expected_session_id = "default"  # US-003: clients join default session
    context.polling_count = 0  # Track number of polling attempts