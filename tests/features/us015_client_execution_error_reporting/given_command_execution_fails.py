def execute(context):
    """Given step: Set up a failed command execution scenario"""
    # Set up test session and client for error reporting
    context.session_id = "test-session-us015"
    context.client_id = "test-client-error"
    context.command_id = "failed-cmd-001"
    
    # Set up error details that would result from a failed command execution
    context.error_message = "Command execution failed: Permission denied"
    context.result_content = None  # No result content for failed commands
    context.execution_duration = 5  # Failed after 5 seconds