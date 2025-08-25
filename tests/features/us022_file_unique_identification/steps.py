from pytest_bdd import scenarios, given, when, then
# 遵循絕對 import 規則 - 不使用相對 import
from tests.features.us022_file_unique_identification import given_multiple_files_with_the_same_name_are_uploaded_to_a_session
from tests.features.us022_file_unique_identification import given_a_file_named_is_uploaded_to_session
from tests.features.us022_file_unique_identification import given_multiple_files_with_identical_names_but_different_content_are_uploaded
from tests.features.us022_file_unique_identification import when_i_query_the_files_in_the_session
from tests.features.us022_file_unique_identification import when_i_query_files_from_both_sessions
from tests.features.us022_file_unique_identification import when_i_query_file_metadata
from tests.features.us022_file_unique_identification import then_each_file_should_have_a_unique_file_id
from tests.features.us022_file_unique_identification import then_i_should_be_able_to_distinguish_files_by_their_metadata
from tests.features.us022_file_unique_identification import then_the_files_should_be_isolated_by_session
from tests.features.us022_file_unique_identification import then_each_file_should_show_unique_file_id_size_and_upload_timestamp
from tests.features.us022_file_unique_identification import then_i_should_be_able_to_select_specific_files_by_their_unique_characteristics

# Load scenarios from feature file
scenarios('story.feature')

@given('multiple files with the same name "test.txt" are uploaded to a session')
def step_given_multiple_files_same_name(context):
    return given_multiple_files_with_the_same_name_are_uploaded_to_a_session.execute(context)

@given('a file named "data.json" is uploaded to session "session-1"')
def step_given_file_uploaded_session_1(context):
    return given_a_file_named_is_uploaded_to_session.execute(context, "data.json", "session-1")

@given('a file named "data.json" is uploaded to session "session-2"')
def step_given_file_uploaded_session_2(context):
    return given_a_file_named_is_uploaded_to_session.execute(context, "data.json", "session-2")

@given('multiple files with identical names but different content are uploaded')
def step_given_identical_names_different_content(context):
    return given_multiple_files_with_identical_names_but_different_content_are_uploaded.execute(context)

@when('I query the files in the session')
def step_when_query_files_in_session(context):
    return when_i_query_the_files_in_the_session.execute(context)

@when('I query files from both sessions')
def step_when_query_files_from_both_sessions(context):
    return when_i_query_files_from_both_sessions.execute(context)

@when('I query file metadata')
def step_when_query_file_metadata(context):
    return when_i_query_file_metadata.execute(context)

@then('each file should have a unique file-id')
def step_then_unique_file_id(context):
    return then_each_file_should_have_a_unique_file_id.execute(context)

@then('I should be able to distinguish files by their metadata')
def step_then_distinguish_by_metadata(context):
    return then_i_should_be_able_to_distinguish_files_by_their_metadata.execute(context)

@then('the files should be isolated by session')
def step_then_isolated_by_session(context):
    return then_the_files_should_be_isolated_by_session.execute(context)

@then('each file should show unique file-id, size, and upload timestamp')
def step_then_show_unique_metadata(context):
    return then_each_file_should_show_unique_file_id_size_and_upload_timestamp.execute(context)

@then('I should be able to select specific files by their unique characteristics')
def step_then_select_by_characteristics(context):
    return then_i_should_be_able_to_select_specific_files_by_their_unique_characteristics.execute(context)