from fastapi import FastAPI
from public_tunnel.routers import client_poll_commands
from public_tunnel.routers import track_client_presence
from public_tunnel.routers import client_offline_threshold_configuration
from public_tunnel.routers import client_offline_status_enforcement
from public_tunnel.routers import command_submit_to_client
from public_tunnel.routers import submit_commands_to_target_clients
from public_tunnel.routers import query_command_execution_status
from public_tunnel.routers import fifo_command_polling
from public_tunnel.routers import client_single_command_retrieval
from public_tunnel.routers import unified_result_query_mechanism
from public_tunnel.routers import client_execution_error_reporting
from public_tunnel.routers import upload_files_to_session
from public_tunnel.routers import download_files_from_session
from public_tunnel.routers import list_session_files
from public_tunnel.routers import session_file_access_isolation

app = FastAPI(
    title="Public Tunnel API",
    description="A network tunneling solution for AI assistants",
    version="0.1.0"
)

# Register routers
app.include_router(client_poll_commands.router)
app.include_router(track_client_presence.router)
app.include_router(command_submit_to_client.router)

# US-016: Client Offline Status Management routers
app.include_router(client_offline_threshold_configuration.router)
app.include_router(client_offline_status_enforcement.router)

# US-006: Targeted Client Command Submission routers
app.include_router(submit_commands_to_target_clients.router)
app.include_router(query_command_execution_status.router)

# US-007: Command FIFO Queue Management routers
app.include_router(fifo_command_polling.router)

# US-009: Client Single Command Retrieval router  
app.include_router(client_single_command_retrieval.router)

# US-021: Unified Result Query Mechanism router
app.include_router(unified_result_query_mechanism.router)

# US-015: Client Execution Error Reporting router
app.include_router(client_execution_error_reporting.router)

# US-010: AI File Upload Feature routers
app.include_router(upload_files_to_session.router)
app.include_router(download_files_from_session.router) 
app.include_router(list_session_files.router)

# US-012: Session File Access Isolation router
app.include_router(session_file_access_isolation.router)


@app.get("/")
async def root():
    return {"message": "Public Tunnel API is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}