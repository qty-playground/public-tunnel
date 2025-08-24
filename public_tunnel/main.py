from fastapi import FastAPI
from public_tunnel.routers import client_poll_commands
from public_tunnel.routers import track_client_presence
from public_tunnel.routers import client_offline_threshold_configuration
from public_tunnel.routers import client_offline_status_enforcement
from public_tunnel.routers import command_submit_to_client

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


@app.get("/")
async def root():
    return {"message": "Public Tunnel API is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}