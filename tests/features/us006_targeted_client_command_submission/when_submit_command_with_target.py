def execute(context):
    """
    Execute the command submission to target client via API
    
    This step calls the API endpoint to submit the command 
    with the target client specified in the request.
    """
    from conftest import BDDPhase
    
    context.phase = BDDPhase.WHEN
    
    # Call the targeted command submission API endpoint
    api_endpoint = f"/api/sessions/{context.session_id}/commands/submit"
    
    response = context.test_client.post(
        api_endpoint,
        json=context.command_request
    )
    
    # Store response for assertions
    context.response = response
    context.status_code = response.status_code
    
    # Try to get JSON response if available
    try:
        context.response_data = response.json()
    except ValueError:
        context.response_data = None