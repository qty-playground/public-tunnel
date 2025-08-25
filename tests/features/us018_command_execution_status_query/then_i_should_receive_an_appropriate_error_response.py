from pytest_bdd import then


@then("I should receive an appropriate error response")
def then_receive_appropriate_error_response(context):
    assert context.status_response.status_code == 404