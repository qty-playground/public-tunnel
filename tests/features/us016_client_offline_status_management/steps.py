from pytest_bdd import scenarios, given, when, then
# 遵循絕對 import 規則 - 不使用相對 import
from tests.features.us016_client_offline_status_management import given_client_has_stopped_polling
from tests.features.us016_client_offline_status_management import when_configured_time_threshold_has_passed
from tests.features.us016_client_offline_status_management import then_client_should_be_marked_as_offline
from tests.features.us016_client_offline_status_management import then_client_should_not_receive_new_commands

# Load scenarios from feature file
scenarios('story.feature')

@given('a client has stopped polling')
def step_given_client_has_stopped_polling(context):
    return given_client_has_stopped_polling.execute(context)

@when('the configured time threshold has passed since last_seen')
def step_when_configured_time_threshold_has_passed(context):
    return when_configured_time_threshold_has_passed.execute(context)

@then('the client should be marked as offline')
def step_then_client_should_be_marked_as_offline(context):
    return then_client_should_be_marked_as_offline.execute(context)

@then('the client should not receive new commands')
def step_then_client_should_not_receive_new_commands(context):
    return then_client_should_not_receive_new_commands.execute(context)