def execute(context):
    """When step: 提交指令到離線的 client"""
    from conftest import BDDPhase
    
    context.phase = BDDPhase.WHEN
    
    # 提交指令到離線的 client
    response = context.test_client.post(
        f"/api/sessions/{context.session_id}/commands/submit",
        json={
            "command_content": context.command_content,
            "target_client_id": context.offline_client_id,
            "timeout_seconds": 30
        }
    )
    
    context.response = response