from pytest_bdd import scenarios, given, when, then
# 遵循絕對 import 規則 - 不使用相對 import
from tests.features.us010_ai_file_upload_feature import given_i_have_a_file_to_share
from tests.features.us010_ai_file_upload_feature import when_i_upload_the_file_to_a_session
from tests.features.us010_ai_file_upload_feature import then_the_file_should_be_stored_with_unique_file_id
from tests.features.us010_ai_file_upload_feature import then_clients_in_the_session_should_be_able_to_download_it

# Load scenarios from feature file
scenarios('story.feature')

@given('I have a file to share')
def step_given_i_have_a_file_to_share(context):
    return given_i_have_a_file_to_share.execute(context)

@when('I upload the file to a session')
def step_when_i_upload_the_file_to_a_session(context):
    return when_i_upload_the_file_to_a_session.execute(context)

@then('the file should be stored with unique file-id')
def step_then_the_file_should_be_stored_with_unique_file_id(context):
    return then_the_file_should_be_stored_with_unique_file_id.execute(context)

@then('clients in the session should be able to download it')
def step_then_clients_in_the_session_should_be_able_to_download_it(context):
    return then_clients_in_the_session_should_be_able_to_download_it.execute(context)