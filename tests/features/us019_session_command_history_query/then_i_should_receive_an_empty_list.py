from pytest_bdd import then


@then("I should receive an empty list")
def then_receive_empty_list(context):
    assert context.history_response.status_code == 200
    history_data = context.history_response.json()
    assert "command_ids" in history_data
    assert isinstance(history_data["command_ids"], list)
    assert len(history_data["command_ids"]) == 0