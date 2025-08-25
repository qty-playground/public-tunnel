from pytest_bdd import given
from public_tunnel.models.command import CommandExecutionStatus


@given("I have submitted a command that is pending execution")
def given_pending_command(context):
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
    
    # Submit a command but don't start execution
    submit_response = context.test_client.post(
        f"/api/sessions/{context.session_id}/commands",
        json={
            "command": "sleep 5",
            "target_client": context.target_client_id
        }
    )
    assert submit_response.status_code == 200
    
    context.command_id = submit_response.json()["command_id"]
    context.expected_status = CommandExecutionStatus.PENDING