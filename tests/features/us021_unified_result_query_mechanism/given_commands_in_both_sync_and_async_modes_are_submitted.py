def execute(context):
    """Given step: Set up both sync and async commands for testing unified result mechanism"""
    # Set up test session and clients
    context.session_id = "test-session-us021"
    context.sync_client_id = "sync-client"
    context.async_client_id = "async-client"
    
    # For API skeleton phase, we just prepare the test data
    # In the implementation phase, we'll submit actual commands
    context.sync_command_id = "sync-cmd-001"
    context.async_command_id = "async-cmd-001"