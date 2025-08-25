from pytest_bdd import scenarios, given, when, then
# 遵循絕對 import 規則 - 不使用相對 import
from tests.features.us004_specified_session_collaboration_mode import given_existing_session_with_session_id
from tests.features.us004_specified_session_collaboration_mode import when_start_polling_with_session_id
from tests.features.us004_specified_session_collaboration_mode import then_join_existing_session
from tests.features.us004_specified_session_collaboration_mode import then_see_other_clients_in_session

# Load scenarios from feature file
scenarios('story.feature')

@given('there is an existing session with specified session-id')
def step_given_existing_session_with_session_id(context):
    return given_existing_session_with_session_id.execute(context)

@when('I start polling with that session-id')
def step_when_start_polling_with_session_id(context):
    return when_start_polling_with_session_id.execute(context)

@then('I should join the existing session')
def step_then_join_existing_session(context):
    return then_join_existing_session.execute(context)

@then('I should be able to see other clients in the same session')
def step_then_see_other_clients_in_session(context):
    return then_see_other_clients_in_session.execute(context)