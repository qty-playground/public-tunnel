from pytest_bdd import when


@when("I query the command history")
def when_query_command_history(context):
    context.history_response = context.test_client.get(
        f"/api/sessions/{context.session_id}/commands/history"
    )