from pytest_bdd import when


@when("I query the command status using that command-id")
def when_query_non_existent_command_status(context):
    context.status_response = context.test_client.get(
        f"/api/sessions/{context.session_id}/commands/{context.command_id}/status"
    )