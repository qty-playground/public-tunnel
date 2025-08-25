def execute(context):
    # Execute GET /api/sessions without admin token
    context.response = context.test_client.get("/api/sessions")