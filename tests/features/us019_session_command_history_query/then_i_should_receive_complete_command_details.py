from pytest_bdd import then


@then("I should receive complete command details")
def then_receive_complete_command_details(context):
    assert context.command_details_response.status_code == 200
    details_data = context.command_details_response.json()
    
    # Verify command details structure
    assert "command_id" in details_data
    assert "execution_status" in details_data
    assert "client_id" in details_data
    assert details_data["command_id"] == context.selected_command_id