from pytest_bdd import scenarios, given, when, then
# 遵循絕對 import 規則 - 不使用相對 import
from tests.features.us008_auto_async_response_with_initial_wait import given_command_is_submitted
from tests.features.us008_auto_async_response_with_initial_wait import when_execution_completes_within_threshold
from tests.features.us008_auto_async_response_with_initial_wait import when_execution_exceeds_threshold
from tests.features.us008_auto_async_response_with_initial_wait import then_result_returned_immediately
from tests.features.us008_auto_async_response_with_initial_wait import then_command_id_returned_for_polling

# Load scenarios from feature file
scenarios('story.feature')

@given('a command is submitted')
def step_given_command_is_submitted(context):
    return given_command_is_submitted.execute(context)

@when('execution completes within the configured threshold')
def step_when_execution_completes_within_threshold(context):
    return when_execution_completes_within_threshold.execute(context)

@when('execution exceeds the threshold')
def step_when_execution_exceeds_threshold(context):
    return when_execution_exceeds_threshold.execute(context)

@then('the result should be returned immediately')
def step_then_result_returned_immediately(context):
    return then_result_returned_immediately.execute(context)

@then('a command-id should be returned for polling')
def step_then_command_id_returned_for_polling(context):
    return then_command_id_returned_for_polling.execute(context)