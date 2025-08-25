def execute(context):
    # Execute GET /api/sessions with invalid admin token
    headers = {"Authorization": context.admin_token}
    context.response = context.test_client.get("/api/sessions", headers=headers)