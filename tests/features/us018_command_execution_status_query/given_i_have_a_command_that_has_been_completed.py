from pytest_bdd import given
from public_tunnel.models.command import CommandExecutionStatus


@given("I have a command that has been completed")
def given_completed_command(context):
    from public_tunnel.dependencies.providers import get_client_presence_tracker
    
    # Set up test data
    context.session_id = "test-session-018"
    context.target_client_id = "client-018"
    
    # Ensure client is online so commands can be submitted
    client_presence_tracker = get_client_presence_tracker()
    client_presence_tracker.update_client_last_seen(
        client_id=context.target_client_id,
        session_id=context.session_id
    )
    
    # For US-018 testing, we'll simulate a completed command by creating a result
    # In a real scenario, this would be the result of actual command execution
    
    # Use a test command_id and create a result for it
    context.command_id = "completed_command_" + "b" * 20  # Make it look UUID-like
    
    # Create a result directly using the result manager
    from public_tunnel.dependencies.providers import get_execution_result_manager
    from public_tunnel.models.execution_result import ExecutionResultStatus
    
    result_manager = get_execution_result_manager()
    result = result_manager.create_and_store_result(
        command_id=context.command_id,
        session_id=context.session_id,
        client_id=context.target_client_id,
        execution_status=ExecutionResultStatus.COMPLETED,
        result_content="test execution completed successfully"
    )
    
    context.expected_status = CommandExecutionStatus.COMPLETED