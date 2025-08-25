def execute(context):
    """
    Upload multiple files with identical names but different content to test metadata distinction
    
    This step creates files with:
    - Same filename
    - Different content (different sizes)
    - Different summaries
    - Different upload timestamps (naturally occurring)
    """
    import base64
    import time
    
    # Set phase to GIVEN to allow state modification
    context.phase = context.phase.__class__.GIVEN
    
    # Set up test session
    context.test_session_id = "test-session-us022-metadata-003"
    context.test_filename = "identical.txt"
    
    # Create multiple files with same name but very different content
    test_files_data = [
        {
            "name": "identical.txt",
            "content": "Small file.",
            "content_type": "text/plain",
            "summary": "Small file for size comparison"
        },
        {
            "name": "identical.txt", 
            "content": "Medium sized file with significantly more content to create a different file size for testing purposes. This file contains multiple sentences and more detailed information to demonstrate how file size can be used as a distinguishing characteristic.",
            "content_type": "text/plain",
            "summary": "Medium-sized file for size comparison"
        },
        {
            "name": "identical.txt",
            "content": """Large file with very substantial content for testing file identification by size and other metadata characteristics. This file contains multiple paragraphs, extensive text content, and detailed information to create a significantly larger file size.

This file serves as an example of how files with identical names can be distinguished through their metadata characteristics such as file size, upload timestamp, content type, and file summary information.

The content includes multiple sections:

Section 1: Introduction to file identification
When multiple files share the same filename, systems must rely on additional metadata to distinguish between them. This is particularly important in scenarios where users might upload files with common names like 'data.txt' or 'report.pdf'.

Section 2: Metadata-based identification
Key metadata fields include:
- File ID (unique identifier)
- File size (bytes)
- Upload timestamp
- Content type
- File summary
- Content hash (when available)

Section 3: Conclusion
By combining these metadata elements, users can reliably identify and select the correct file even when filenames are identical.

This concludes the large file content for testing purposes.""",
            "content_type": "text/plain", 
            "summary": "Large detailed file for comprehensive size comparison"
        }
    ]
    
    # Initialize response storage
    context.upload_responses = []
    context.expected_files_count = len(test_files_data)
    
    # Upload each file via HTTP API with small delays to ensure different timestamps
    for i, file_data in enumerate(test_files_data):
        # Small delay to ensure different upload timestamps
        if i > 0:
            time.sleep(0.1)
        
        # Encode content to Base64
        file_content_base64 = base64.b64encode(
            file_data["content"].encode('utf-8')
        ).decode('utf-8')
        
        # Prepare upload request
        upload_request = {
            "file_name": file_data["name"],
            "file_content_base64": file_content_base64,
            "content_type": file_data["content_type"],
            "file_summary": file_data["summary"]
        }
        
        # Upload file via HTTP API
        response = context.test_client.post(
            f"/api/sessions/{context.test_session_id}/files",
            json=upload_request
        )
        
        # Store response for later verification
        context.upload_responses.append(response)