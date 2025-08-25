from pytest_bdd import then


@then("I should be able to query details for each command")
def then_able_to_query_details_for_each_command(context):
    history_data = context.history_response.json()
    
    # Test that we can query details for each command_id in the history
    for command_id in history_data["command_ids"]:
        details_response = context.test_client.get(
            f"/api/sessions/{context.session_id}/commands/{command_id}/status"
        )
        assert details_response.status_code == 200
        
        details_data = details_response.json()
        assert details_data["command_id"] == command_id
        assert "execution_status" in details_data