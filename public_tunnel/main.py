from fastapi import FastAPI
from public_tunnel.routers import client_poll_commands
from public_tunnel.routers import track_client_presence

app = FastAPI(
    title="Public Tunnel API",
    description="A network tunneling solution for AI assistants",
    version="0.1.0"
)

# Register routers
app.include_router(client_poll_commands.router)
app.include_router(track_client_presence.router)


@app.get("/")
async def root():
    return {"message": "Public Tunnel API is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}