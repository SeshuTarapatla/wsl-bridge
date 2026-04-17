from fastapi import FastAPI

from wsl_bridge.scrcpy import scrcpy_router

app = FastAPI(title="wsl-bridge")
app.include_router(scrcpy_router)


@app.get("/")
def status() -> bool:
    return True
