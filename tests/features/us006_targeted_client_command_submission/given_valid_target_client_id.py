def execute(context):
    """
    Set up test scenario with a valid target client-id
    
    This step prepares the test context with:
    - A valid session ID
    - A valid target client ID  
    - Test command content
    """
    from conftest import BDDPhase
    
    context.phase = BDDPhase.GIVEN
    
    # Set up test data for command submission
    context.session_id = "test-session-001"
    context.target_client_id = "client-001"
    context.command_content = "echo 'test command for targeted submission'"
    context.timeout_seconds = 30
    
    # Prepare request payload for API call
    context.command_request = {
        "command_content": context.command_content,
        "target_client_id": context.target_client_id,
        "timeout_seconds": context.timeout_seconds
    }