from fastapi import FastAPI
from my_modules.logger import get_logger

from wsl_bridge.scrcpy import scrcpy_router

app = FastAPI(title="wsl-bridge")
app.include_router(scrcpy_router)
get_logger("uvicorn")
get_logger("uvicorn.access")
get_logger("uvicorn.error")


@app.get("/")
def status() -> bool:
    return True
