from pytest_bdd import scenarios, given, when, then
# 遵循絕對 import 規則 - 不使用相對 import
from tests.features.us006_targeted_client_command_submission import given_valid_target_client_id
from tests.features.us006_targeted_client_command_submission import when_submit_command_with_target
from tests.features.us006_targeted_client_command_submission import then_command_queued_for_client
from tests.features.us006_targeted_client_command_submission import then_only_target_client_receives_command

# Load scenarios from feature file
scenarios('story.feature')

@given('I have a valid target client-id')
def step_given_valid_target_client_id(context):
    return given_valid_target_client_id.execute(context)

@when('I submit a command with target_client specified')
def step_when_submit_command_with_target(context):
    return when_submit_command_with_target.execute(context)

@then('the command should be queued for that specific client')
def step_then_command_queued_for_client(context):
    return then_command_queued_for_client.execute(context)

@then('only that client should receive the command')
def step_then_only_target_client_receives_command(context):
    return then_only_target_client_receives_command.execute(context)