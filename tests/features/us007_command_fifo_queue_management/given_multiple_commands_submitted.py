def execute(context):
    """
    Setup multiple commands to be submitted to the same client
    
    This step prepares the test context with:
    - Registered client (required by US-013)
    - Multiple command submissions to the same target client
    - Records the submission order for FIFO verification
    """
    from conftest import BDDPhase
    from public_tunnel.dependencies.providers import get_client_presence_tracker
    
    context.phase = BDDPhase.GIVEN
    
    # Set up test data
    context.session_id = "test-session-fifo"
    context.target_client_id = "client-fifo-test"
    context.timeout_seconds = 30
    
    # US-013 requirement: Client must register (via polling) before receiving commands
    # Simulate client registration by updating client presence
    client_presence_tracker = get_client_presence_tracker()
    client_presence_tracker.update_client_last_seen(
        client_id=context.target_client_id,
        session_id=context.session_id
    )
    
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