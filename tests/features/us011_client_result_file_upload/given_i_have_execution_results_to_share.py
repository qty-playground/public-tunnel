import base64

def execute(context):
    """Set up execution results that need to be shared with AI"""
    # Given: I have execution results to share
    context.session_id = "test-session-001"
    context.command_id = "cmd-with-files-001"
    
    # Prepare test files as execution results
    context.test_result_content = "Command executed successfully with output files"
    
    # Test file 1: A text log file
    log_content = "Execution log:\n2023-11-24 10:00:00 - Command started\n2023-11-24 10:00:05 - Command completed"
    context.log_file_base64 = base64.b64encode(log_content.encode()).decode()
    
    # Test file 2: A JSON report file
    report_content = '{"status": "success", "execution_time": 5.2, "output_lines": 42}'
    context.report_file_base64 = base64.b64encode(report_content.encode()).decode()
    
    # Store expected file data for verification
    context.expected_files = [
        {
            "file_name": "execution.log",
            "content_type": "text/plain",
            "file_summary": "Execution log with timestamps",
            "content": log_content
        },
        {
            "file_name": "report.json", 
            "content_type": "application/json",
            "file_summary": "Execution report with metrics",
            "content": report_content
        }
    ]