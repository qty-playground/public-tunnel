def execute(context):
    # Verify that response is 403 Forbidden
    assert context.response.status_code == 403, f"Expected 403 Forbidden, got {context.response.status_code}"