from pytest_bdd import given
from public_tunnel.dependencies.providers import get_client_presence_tracker, get_execution_result_manager
from public_tunnel.models.execution_result import ExecutionResultStatus


@given("commands have been executed in a session")
def given_commands_executed_in_session(context):
    from public_tunnel.dependencies.providers import get_client_presence_tracker
    
    # Set up test data
    context.session_id = "test-session-019"
    context.target_client_id = "client-019"
    
    # Ensure client is online so commands can be submitted
    client_presence_tracker = get_client_presence_tracker()
    client_presence_tracker.update_client_last_seen(
        client_id=context.target_client_id,
        session_id=context.session_id
    )
    
    # Submit multiple commands to create history
    context.executed_commands = []
    commands = ["echo 'first command'", "ls", "pwd"]
    
    for i, cmd in enumerate(commands):
        # Submit command
        submit_response = context.test_client.post(
            f"/api/sessions/{context.session_id}/commands",
            json={
                "command": cmd,
                "target_client": context.target_client_id
            }
        )
        assert submit_response.status_code == 200
        command_id = submit_response.json()["command_id"]
        
        # Create execution result for the command
        result_manager = get_execution_result_manager()
        result = result_manager.create_and_store_result(
            command_id=command_id,
            session_id=context.session_id,
            client_id=context.target_client_id,
            execution_status=ExecutionResultStatus.COMPLETED,
            result_content=f"Result for: {cmd}"
        )
        
        context.executed_commands.append({
            "command_id": command_id,
            "command": cmd,
            "result": result
        })