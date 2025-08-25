from pytest_bdd import then
from public_tunnel.models.command import CommandExecutionStatus


@then("I should know that the command is running")
def then_command_is_running(context):
    response_data = context.status_response.json()
    assert response_data["execution_status"] == CommandExecutionStatus.RUNNING