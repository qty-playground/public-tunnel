from pytest_bdd import scenarios, given, when, then
# 遵循絕對 import 規則 - 不使用相對 import
from tests.features.us007_command_fifo_queue_management import given_multiple_commands_submitted
from tests.features.us007_command_fifo_queue_management import when_client_polls_for_commands
from tests.features.us007_command_fifo_queue_management import then_commands_returned_in_fifo_order
from tests.features.us007_command_fifo_queue_management import then_each_polling_returns_one_command

# Load scenarios from feature file
scenarios('story.feature')

@given('multiple commands are submitted to the same client')
def step_given_multiple_commands_submitted(context):
    return given_multiple_commands_submitted.execute(context)

@when('the client polls for commands')
def step_when_client_polls_for_commands(context):
    return when_client_polls_for_commands.execute(context)

@then('commands should be returned in first-in-first-out order')
def step_then_commands_returned_in_fifo_order(context):
    return then_commands_returned_in_fifo_order.execute(context)

@then('each polling should return only one command')
def step_then_each_polling_returns_one_command(context):
    return then_each_polling_returns_one_command.execute(context)