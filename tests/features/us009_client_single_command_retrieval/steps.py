from pytest_bdd import scenarios, given, when, then
# 遵循絕對 import 規則 - 不使用相對 import
from tests.features.us009_client_single_command_retrieval import given_multiple_commands_in_queue
from tests.features.us009_client_single_command_retrieval import when_send_polling_request
from tests.features.us009_client_single_command_retrieval import then_receive_exactly_one_command
from tests.features.us009_client_single_command_retrieval import then_command_removed_from_queue

# Load scenarios from feature file
scenarios('story.feature')

@given('there are multiple commands in my queue')
def step_given_multiple_commands_in_queue(context):
    return given_multiple_commands_in_queue.execute(context)

@when('I send a polling request')
def step_when_send_polling_request(context):
    return when_send_polling_request.execute(context)

@then('I should receive exactly one command')
def step_then_receive_exactly_one_command(context):
    return then_receive_exactly_one_command.execute(context)

@then('that command should be removed from the queue')
def step_then_command_removed_from_queue(context):
    return then_command_removed_from_queue.execute(context)