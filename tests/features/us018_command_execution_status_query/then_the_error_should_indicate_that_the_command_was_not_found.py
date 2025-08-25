from pytest_bdd import then


@then("the error should indicate that the command was not found")
def then_error_indicates_command_not_found(context):
    response_data = context.status_response.json()
    assert "detail" in response_data
    assert "not found" in response_data["detail"].lower()