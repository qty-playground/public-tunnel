from conftest import BDDPhase

def execute(context):
    """Execute polling with the specified session-id"""
    context.phase = BDDPhase.WHEN
    
    # Send polling request with the target session-id
    # This should join the new client to the existing session
    polling_response = context.test_client.post(
        f"/api/sessions/{context.target_session_id}/poll",
        json={"client_id": context.new_client_id}
    )
    
    context.polling_result = {
        "response": polling_response,
        "status_code": polling_response.status_code,
        "response_data": polling_response.json() if polling_response.status_code == 200 else None
    }