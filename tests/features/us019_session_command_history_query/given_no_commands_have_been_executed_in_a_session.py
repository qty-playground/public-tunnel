from pytest_bdd import given


@given("no commands have been executed in a session")
def given_no_commands_executed_in_session(context):
    # Set up test data for empty session
    context.session_id = "empty-session-019" 
    context.target_client_id = "client-019"
    context.executed_commands = []