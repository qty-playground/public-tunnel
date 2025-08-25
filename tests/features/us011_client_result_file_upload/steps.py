from pytest_bdd import scenarios, given, when, then
# 遵循絕對 import 規則 - 不使用相對 import
from tests.features.us011_client_result_file_upload import given_i_have_execution_results_to_share
from tests.features.us011_client_result_file_upload import when_i_upload_files_as_part_of_result_reporting
from tests.features.us011_client_result_file_upload import then_each_file_should_have_file_id_filename_and_summary
from tests.features.us011_client_result_file_upload import then_the_ai_should_be_able_to_browse_and_download_selectively

# Load scenarios from feature file
scenarios('story.feature')

@given('I have execution results to share')
def step_given_execution_results_to_share(context):
    return given_i_have_execution_results_to_share.execute(context)

@when('I upload files as part of result reporting')
def step_when_upload_files_as_result_reporting(context):
    return when_i_upload_files_as_part_of_result_reporting.execute(context)

@then('each file should have file-id, filename, and summary')
def step_then_file_has_metadata(context):
    return then_each_file_should_have_file_id_filename_and_summary.execute(context)

@then('the AI should be able to browse and download selectively')
def step_then_ai_can_browse_and_download(context):
    return then_the_ai_should_be_able_to_browse_and_download_selectively.execute(context)