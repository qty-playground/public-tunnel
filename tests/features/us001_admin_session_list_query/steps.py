from pytest_bdd import scenarios, given, when, then
# 遵循絕對 import 規則 - 不使用相對 import
from tests.features.us001_admin_session_list_query import given_admin_token
from tests.features.us001_admin_session_list_query import given_sessions_exist  
from tests.features.us001_admin_session_list_query import given_no_sessions
from tests.features.us001_admin_session_list_query import when_query_sessions
from tests.features.us001_admin_session_list_query import then_receive_session_list
from tests.features.us001_admin_session_list_query import then_verify_metadata
from tests.features.us001_admin_session_list_query import then_receive_empty_list
from tests.features.us001_admin_session_list_query import then_success_status

# Load scenarios from feature file
scenarios('story.feature')

@given('I have a valid admin token')
def step_given_valid_admin_token(context):
    return given_admin_token.execute(context)

@given('there are multiple sessions in the system')
def step_given_multiple_sessions(context):
    return given_sessions_exist.execute(context)

@given('there are no sessions in the system')
def step_given_no_sessions(context):
    return given_no_sessions.execute(context)

@when('I query GET /api/sessions with admin token')
def step_when_query_sessions_with_admin_token(context):
    return when_query_sessions.execute(context)

@then('I should receive a list of all sessions')
def step_then_receive_all_sessions(context):
    return then_receive_session_list.execute(context)

@then('each session should include basic metadata')
def step_then_verify_session_metadata(context):
    return then_verify_metadata.execute(context)

@then('I should receive an empty session list')
def step_then_receive_empty_session_list(context):
    return then_receive_empty_list.execute(context)

@then('the response status should be success')
def step_then_response_success(context):
    return then_success_status.execute(context)