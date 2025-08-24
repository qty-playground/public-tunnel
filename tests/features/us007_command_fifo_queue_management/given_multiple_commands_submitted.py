def execute(context):
    """
    Setup multiple commands to be submitted to the same client
    
    This step prepares the test context with:
    - Multiple command submissions to the same target client
    - Records the submission order for FIFO verification
    """
    from conftest import BDDPhase
    
    context.phase = BDDPhase.GIVEN
    
    # Set up test data
    context.session_id = "test-session-fifo"
    context.target_client_id = "client-fifo-test"
    context.timeout_seconds = 30
    
    # Define multiple commands in specific order
    context.test_commands = [
        "echo 'First command'",
        "echo 'Second command'", 
        "echo 'Third command'"
    ]
    
    # Submit commands to target client using US-006 API
    context.submitted_commands = []
    context.submission_responses = []
    
    api_endpoint = f"/api/sessions/{context.session_id}/commands/submit"
    
    for i, command_content in enumerate(context.test_commands):
        command_request = {
            "command_content": command_content,
            "target_client_id": context.target_client_id,
            "timeout_seconds": context.timeout_seconds
        }
        
        response = context.test_client.post(api_endpoint, json=command_request)
        
        context.submission_responses.append(response)
        context.submitted_commands.append({
            "order": i,
            "content": command_content,
            "response": response,
            "command_id": response.json().get("command_id") if response.status_code == 200 else None
        })