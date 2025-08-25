def execute(context):
    # Verify that response status is success (200 OK)
    assert context.response.status_code == 200, f"Expected 200 OK, got {context.response.status_code}"