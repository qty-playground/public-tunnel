from pytest_bdd import then


@then("the details should include execution status and results")
def then_details_include_execution_status_and_results(context):
    details_data = context.command_details_response.json()
    
    # Verify essential fields are present
    assert "execution_status" in details_data
    assert "command_id" in details_data
    
    # For completed commands, there should be result information available
    if details_data["execution_status"] == "completed":
        # The command details should have either result_summary or we should be able to get results
        # via the unified result query mechanism
        result_response = context.test_client.get(
            f"/api/sessions/{context.session_id}/results/{context.selected_command_id}"
        )
        assert result_response.status_code == 200