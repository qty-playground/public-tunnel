def execute(context):
    """
    Send a polling request to retrieve single command via US-009 API endpoint
    
    This step performs ONLY the action - making the API call.
    All verifications should be done in the Then steps.
    """
    # Use the test client from pytest setup to make API call
    api_endpoint = f"/api/sessions/{context.test_session_id}/clients/{context.test_client_id}/command"
    
    response = context.test_client.get(api_endpoint)
    
    # Store response for verification in subsequent steps
    context.api_response = response
    context.response_data = response.json() if response.status_code == 200 else None