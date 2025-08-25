def execute(context):
    # Execute GET /api/sessions with admin token
    headers = {"Authorization": context.valid_admin_token}
    context.response = context.test_client.get("/api/sessions", headers=headers)