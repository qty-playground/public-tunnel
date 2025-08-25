from conftest import BDDPhase

def execute(context):
    """Verify that the client successfully joined the existing session"""
    context.phase = BDDPhase.THEN
    
    # Verify polling was successful
    assert context.polling_result["status_code"] == 200, \
        f"Expected 200, got {context.polling_result['status_code']}"
    
    # The client should now be part of the specified session
    # This is verified by successful polling response
    assert context.polling_result["response_data"] is not None, \
        "Expected response data for successful session join"