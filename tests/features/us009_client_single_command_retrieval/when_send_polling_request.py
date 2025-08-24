def execute(context):
    """
    Send a polling request to retrieve single command via US-009 API endpoint
    
    This step performs the actual API call to the US-009 client-focused endpoint
    and captures the response for verification.
    """
    # Use the test client from pytest setup to make API call
    api_endpoint = f"/api/sessions/{context.test_session_id}/clients/{context.test_client_id}/command"
    
    response = context.test_client.get(api_endpoint)
    
    # Store response for verification in subsequent steps
    context.api_response = response
    context.response_data = response.json() if response.status_code == 200 else None
    
    # Store initial queue state for verification
    from public_tunnel.dependencies.providers import get_command_queue_manager
    queue_manager = get_command_queue_manager()
    context.queue_size_after_request = queue_manager.get_queue_size_for_client(
        context.test_session_id, 
        context.test_client_id
    )