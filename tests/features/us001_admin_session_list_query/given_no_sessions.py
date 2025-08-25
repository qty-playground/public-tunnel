def execute(context):
    # Note: System always has at least a default session
    # This scenario tests the case where only default session exists
    # and no additional sessions have been created
    context.expected_sessions_exist = True
    context.minimum_sessions = 1  # At least default session should exist