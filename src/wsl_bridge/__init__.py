import uvicorn

from wsl_bridge.base import app


def main():
    uvicorn.run(app)
