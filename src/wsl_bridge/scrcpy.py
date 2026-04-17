from subprocess import Popen

from fastapi import APIRouter
from my_modules.scrcpy import Scrcpy
from pydantic import BaseModel

scrcpy_router = APIRouter(prefix="/scrcpy")


class ScrcpyStartResponse(BaseModel):
    status: str
    pid: int


class ScrcpyController:
    def __init__(self) -> None:
        self.proc: Popen[bytes] | None = None

    def start(self, serial: str) -> ScrcpyStartResponse:
        self.stop()
        self.proc = Scrcpy(serial).start()
        return ScrcpyStartResponse(status="started", pid=self.proc.pid)

    def stop(self) -> bool:
        if self.proc:
            self.proc = self.proc.terminate()
            return True
        return False

    def status(self) -> bool:
        return bool(self.proc)


scrcpy = ScrcpyController()


@scrcpy_router.get("/")
async def status():
    return scrcpy.status()


@scrcpy_router.post("/start", response_model=ScrcpyStartResponse)
async def start(serial: str) -> ScrcpyStartResponse:
    return scrcpy.start(serial)


@scrcpy_router.post("/stop")
async def stop() -> bool:
    return scrcpy.stop()
