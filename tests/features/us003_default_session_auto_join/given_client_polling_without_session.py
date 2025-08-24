def execute(context):
    # Set up a client that will poll without specifying session-id
    # Store client_id in context for subsequent steps
    context.client_id = "test-client-001"
    context.polling_endpoint = "/api/sessions/default/poll"