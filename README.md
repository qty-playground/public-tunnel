# Public Tunnel

A network tunneling solution designed for AI assistants to control devices in non-directly accessible network environments.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn public_tunnel.main:app --reload
```

## Testing

```bash
# Run tests
pytest

# Run with verbose output
pytest -v
```

## Project Structure

- `public_tunnel/` - Main application module
- `tests/` - Test cases with pytest-bdd support
- `docs/` - Project documentation and analysis