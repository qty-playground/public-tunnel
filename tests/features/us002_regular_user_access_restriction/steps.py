from pytest_bdd import scenarios, given, when, then
# 遵循絕對 import 規則 - 不使用相對 import
from tests.features.us002_regular_user_access_restriction import given_no_admin_token
from tests.features.us002_regular_user_access_restriction import given_invalid_admin_token  
from tests.features.us002_regular_user_access_restriction import when_query_sessions_no_token
from tests.features.us002_regular_user_access_restriction import when_query_sessions_invalid_token
from tests.features.us002_regular_user_access_restriction import then_forbidden_response
from tests.features.us002_regular_user_access_restriction import then_no_session_info

# Load scenarios from feature file
scenarios('story.feature')

@given("I don't have a valid admin token")
def step_given_no_valid_admin_token(context):
    return given_no_admin_token.execute(context)

@given('I have an invalid admin token')
def step_given_invalid_admin_token(context):
    return given_invalid_admin_token.execute(context)

@when('I query GET /api/sessions')
def step_when_query_sessions_without_token(context):
    return when_query_sessions_no_token.execute(context)

@when('I query GET /api/sessions with invalid token')
def step_when_query_sessions_with_invalid_token(context):
    return when_query_sessions_invalid_token.execute(context)

@then('I should receive a 403 Forbidden response')
def step_then_receive_403_forbidden(context):
    return then_forbidden_response.execute(context)

@then('I should not see any session information')
def step_then_no_session_information(context):
    return then_no_session_info.execute(context)