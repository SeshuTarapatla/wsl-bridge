import uvicorn

from wsl_bridge.base import app
from wsl_bridge.vars import SERVER_HOST, SERVER_PORT


def main():
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)
