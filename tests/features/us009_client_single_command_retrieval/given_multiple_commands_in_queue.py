def execute(context):
    """
    Set up test context with multiple commands queued for a specific client
    
    This step prepares the test environment by:
    1. Setting up a test session and client
    2. Submitting multiple commands to the client's queue
    3. Storing the test data in context for later verification
    """
    # Set up test data
    context.test_session_id = "test-session-001"
    context.test_client_id = "test-client-001"
    
    # Get the command queue manager from the test application
    # This will use the same instance as the API endpoints
    from public_tunnel.dependencies.providers import get_command_queue_manager
    queue_manager = get_command_queue_manager()
    
    # Submit three test commands to create a queue using the service method
    test_command_contents = [
        "echo 'first command'",
        "ls -la", 
        "pwd"
    ]
    
    # Add commands to the queue and store references for later verification
    context.test_commands = []
    for command_content in test_command_contents:
        command = queue_manager.submit_command_to_target_client(
            session_id=context.test_session_id,
            target_client_id=context.test_client_id,
            command_content=command_content
        )
        context.test_commands.append(command)
    
