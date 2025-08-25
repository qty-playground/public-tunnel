from pytest_bdd import scenarios, given, when, then
# 遵循絕對 import 規則 - 不使用相對 import
from tests.features.us015_client_execution_error_reporting import given_command_execution_fails
from tests.features.us015_client_execution_error_reporting import when_report_the_result
from tests.features.us015_client_execution_error_reporting import then_error_formatted_like_normal_result
from tests.features.us015_client_execution_error_reporting import then_ai_can_query_error_like_any_result

# Load scenarios from feature file
scenarios('story.feature')

@given('a command execution fails')
def step_given_command_execution_fails(context):
    return given_command_execution_fails.execute(context)

@when('I report the result')
def step_when_report_the_result(context):
    return when_report_the_result.execute(context)

@then('the error should be formatted like a normal result')
def step_then_error_formatted_like_normal_result(context):
    return then_error_formatted_like_normal_result.execute(context)

@then('the AI should be able to query the error like any result')
def step_then_ai_can_query_error_like_any_result(context):
    return then_ai_can_query_error_like_any_result.execute(context)