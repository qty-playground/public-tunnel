from pytest_bdd import scenarios, given, when, then
# 遵循絕對 import 規則 - 不使用相對 import
from tests.features.us014_offline_client_command_rejection import given_client_is_marked_as_offline
from tests.features.us014_offline_client_command_rejection import when_command_targets_that_client
from tests.features.us014_offline_client_command_rejection import then_return_error_indicating_client_is_offline
from tests.features.us014_offline_client_command_rejection import then_command_should_not_be_queued

# Load scenarios from feature file
scenarios('story.feature')

@given('a client is marked as offline')
def step_given_client_is_marked_as_offline(context):
    return given_client_is_marked_as_offline.execute(context)

@when('a command targets that client')
def step_when_command_targets_that_client(context):
    return when_command_targets_that_client.execute(context)

@then('I should return an error indicating client is offline')
def step_then_return_error_indicating_client_is_offline(context):
    return then_return_error_indicating_client_is_offline.execute(context)

@then('the command should not be queued')
def step_then_command_should_not_be_queued(context):
    return then_command_should_not_be_queued.execute(context)