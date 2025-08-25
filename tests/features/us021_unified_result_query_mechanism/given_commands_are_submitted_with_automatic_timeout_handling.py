def execute(context):
    """Given step: Set up commands for testing unified result mechanism"""
    # Set up test session and clients
    context.session_id = "test-session-us021"
    context.fast_client_id = "fast-client"  # For commands that complete quickly
    context.slow_client_id = "slow-client"  # For commands that may timeout
    
    # For API skeleton phase, we just prepare the test data
    # In the implementation phase, we'll submit actual commands
    context.fast_command_id = "fast-cmd-001"
    context.slow_command_id = "slow-cmd-001"