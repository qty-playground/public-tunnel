from fastapi import FastAPI

app = FastAPI(
    title="Public Tunnel API",
    description="A network tunneling solution for AI assistants",
    version="0.1.0"
)


@app.get("/")
async def root():
    return {"message": "Public Tunnel API is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}