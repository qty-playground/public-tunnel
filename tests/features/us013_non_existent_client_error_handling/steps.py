from pytest_bdd import scenarios, given, when, then
# 遵循絕對 import 規則 - 不使用相對 import
from tests.features.us013_non_existent_client_error_handling import given_command_targets_non_existent_client
from tests.features.us013_non_existent_client_error_handling import when_command_is_submitted
from tests.features.us013_non_existent_client_error_handling import then_return_appropriate_error_response
from tests.features.us013_non_existent_client_error_handling import then_command_should_not_be_queued

# Load scenarios from feature file
scenarios('story.feature')

@given('a command targets a non-existent client-id')
def step_given_command_targets_non_existent_client(context):
    return given_command_targets_non_existent_client.execute(context)

@when('the command is submitted')
def step_when_command_is_submitted(context):
    return when_command_is_submitted.execute(context)

@then('I should return an appropriate error response')
def step_then_return_appropriate_error_response(context):
    return then_return_appropriate_error_response.execute(context)

@then('the command should not be queued')
def step_then_command_should_not_be_queued(context):
    return then_command_should_not_be_queued.execute(context)