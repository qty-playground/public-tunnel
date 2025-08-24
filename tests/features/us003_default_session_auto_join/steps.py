from pytest_bdd import scenarios, given, when, then
# 遵循絕對 import 規則 - 不使用相對 import
from tests.features.us003_default_session_auto_join import given_client_polling_without_session
from tests.features.us003_default_session_auto_join import when_send_first_polling_request
from tests.features.us003_default_session_auto_join import then_assigned_to_default_session
from tests.features.us003_default_session_auto_join import then_client_id_recorded

# Load scenarios from feature file
scenarios('story.feature')

@given('I start polling without specifying session-id')
def step_given_client_polling_without_session(context):
    return given_client_polling_without_session.execute(context)

@when('I send my first polling request')
def step_when_send_first_polling_request(context):
    return when_send_first_polling_request.execute(context)

@then('I should be automatically assigned to default session')
def step_then_assigned_to_default_session(context):
    return then_assigned_to_default_session.execute(context)

@then('my client-id should be recorded in the session')
def step_then_client_id_recorded(context):
    return then_client_id_recorded.execute(context)