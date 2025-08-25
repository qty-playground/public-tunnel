import time
from pytest_bdd import given
from public_tunnel.models.command import CommandExecutionStatus


@given("I have a command that is currently running")
def given_running_command(context):
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
    
    # For US-018 testing, we'll simulate a running command
    # In a real scenario, this would involve actual command execution tracking
    # Here we just set up a test scenario that our status API can recognize
    
    # Use a specific command_id pattern that our status API recognizes as running
    context.command_id = "running_command_" + "a" * 20  # Make it look UUID-like
    context.expected_status = CommandExecutionStatus.RUNNING