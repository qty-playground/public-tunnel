from pytest_bdd import scenarios, given, when, then
# 遵循絕對 import 規則 - 不使用相對 import
from tests.features.us021_unified_result_query_mechanism import given_commands_are_submitted_with_automatic_timeout_handling
from tests.features.us021_unified_result_query_mechanism import when_results_are_generated_from_command_execution
from tests.features.us021_unified_result_query_mechanism import then_all_results_should_be_stored_with_command_id_indexing
from tests.features.us021_unified_result_query_mechanism import then_results_should_be_queryable_through_the_same_api

# Load scenarios from feature file
scenarios('story.feature')

@given('commands are submitted (with automatic timeout handling)')
def step_given_commands_submitted_with_timeout(context):
    return given_commands_are_submitted_with_automatic_timeout_handling.execute(context)

@when('results are generated from command execution')
def step_when_results_are_generated(context):
    return when_results_are_generated_from_command_execution.execute(context)

@then('all results should be stored with command-id indexing')
def step_then_results_stored_with_command_id_indexing(context):
    return then_all_results_should_be_stored_with_command_id_indexing.execute(context)

@then('results should be queryable through the same API')
def step_then_results_queryable_through_same_api(context):
    return then_results_should_be_queryable_through_the_same_api.execute(context)

@then('results should be queryable through the same API regardless of execution time')
def step_then_results_queryable_regardless_of_time(context):
    return then_results_should_be_queryable_through_the_same_api.execute(context)