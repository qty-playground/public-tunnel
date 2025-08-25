from pytest_bdd import then


@then("I should receive current execution status")
def then_receive_current_execution_status(context):
    assert context.status_response.status_code == 200
    response_data = context.status_response.json()
    assert "execution_status" in response_data
    assert "command_id" in response_data
    assert response_data["command_id"] == context.command_id