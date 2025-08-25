from pytest_bdd import scenarios, given, when, then
# 遵循絕對 import 規則 - 不使用相對 import
from tests.features.us012_session_file_access_isolation import given_files_are_uploaded_to_a_session
from tests.features.us012_session_file_access_isolation import when_users_try_to_access_files
from tests.features.us012_session_file_access_isolation import then_only_users_within_the_same_session_should_have_access
from tests.features.us012_session_file_access_isolation import then_cross_session_file_access_should_be_denied

# Load scenarios from feature file
scenarios('story.feature')

@given('files are uploaded to a session')
def step_given_files_are_uploaded_to_a_session(context):
    return given_files_are_uploaded_to_a_session.execute(context)

@when('users try to access files')
def step_when_users_try_to_access_files(context):
    return when_users_try_to_access_files.execute(context)

@then('only users within the same session should have access')
def step_then_only_users_within_the_same_session_should_have_access(context):
    return then_only_users_within_the_same_session_should_have_access.execute(context)

@then('cross-session file access should be denied')
def step_then_cross_session_file_access_should_be_denied(context):
    return then_cross_session_file_access_should_be_denied.execute(context)