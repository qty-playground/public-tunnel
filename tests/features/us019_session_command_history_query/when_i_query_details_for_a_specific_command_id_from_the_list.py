from pytest_bdd import when


@when("I query details for a specific command-id from the list")
def when_query_specific_command_details(context):
    # Get the first command_id from the history response
    history_data = context.history_response.json()
    context.selected_command_id = history_data["command_ids"][0]
    
    # Query details for this specific command using the existing status API
    context.command_details_response = context.test_client.get(
        f"/api/sessions/{context.session_id}/commands/{context.selected_command_id}/status"
    )