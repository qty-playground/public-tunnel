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


@app.get("/")
async def root():
    return {"message": "Public Tunnel API is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}