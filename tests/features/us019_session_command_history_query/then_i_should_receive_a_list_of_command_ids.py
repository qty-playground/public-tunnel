from pytest_bdd import then


@then("I should receive a list of command-ids")
def then_receive_list_of_command_ids(context):
    assert context.history_response.status_code == 200
    history_data = context.history_response.json()
    assert "command_ids" in history_data
    assert isinstance(history_data["command_ids"], list)
    assert len(history_data["command_ids"]) == len(context.executed_commands)
    
    # Verify all executed command IDs are in the history
    expected_command_ids = [cmd["command_id"] for cmd in context.executed_commands]
    for command_id in expected_command_ids:
        assert command_id in history_data["command_ids"]