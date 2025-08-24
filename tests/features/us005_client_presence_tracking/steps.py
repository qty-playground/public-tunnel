from pytest_bdd import scenarios, given, when, then
# 遵循絕對 import 規則 - 不使用相對 import
from tests.features.us005_client_presence_tracking import given_client_is_polling_regularly
from tests.features.us005_client_presence_tracking import when_client_sends_polling_requests
from tests.features.us005_client_presence_tracking import then_update_last_seen_timestamp
from tests.features.us005_client_presence_tracking import then_client_marked_as_online

# Load scenarios from feature file
scenarios('story.feature')

@given('a client is polling regularly')
def step_given_client_is_polling_regularly(context):
    return given_client_is_polling_regularly.execute(context)

@when('the client sends polling requests')
def step_when_client_sends_polling_requests(context):
    return when_client_sends_polling_requests.execute(context)

@then('I should update the client\'s last_seen timestamp')
def step_then_update_last_seen_timestamp(context):
    return then_update_last_seen_timestamp.execute(context)

@then('the client should be marked as online')
def step_then_client_marked_as_online(context):
    return then_client_marked_as_online.execute(context)