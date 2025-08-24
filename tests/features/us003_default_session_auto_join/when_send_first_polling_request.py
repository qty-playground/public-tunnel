def execute(context):
    # Send the first polling request to the server
    response = context.test_client.get(
        context.polling_endpoint,
        params={"client_id": context.client_id}
    )
    context.response = response