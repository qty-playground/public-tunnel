from pytest_bdd import given


@given("I have a non-existent command-id")
def given_non_existent_command_id(context):
    # Set up test data
    context.session_id = "test-session-018"
    context.target_client_id = "client-018"
    
    context.command_id = "non_existent_command_id_12345"