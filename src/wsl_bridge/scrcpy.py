from subprocess import Popen

from fastapi import APIRouter
from httpx import get, post
from my_modules.scrcpy import Scrcpy
from pydantic import BaseModel

from wsl_bridge.vars import URL

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
        if self.proc and self.proc.poll() is None:
            return True
        return False


scrcpy = ScrcpyController()


@scrcpy_router.get("/")
def status():
    return scrcpy.status()


@scrcpy_router.post("/start", response_model=ScrcpyStartResponse)
def start(serial: str) -> ScrcpyStartResponse:
    return scrcpy.start(serial)


@scrcpy_router.post("/stop")
def stop() -> bool:
    return scrcpy.stop()


class ScrcpyClient:
    url = f"{URL}/scrcpy"

    @classmethod
    def start(cls, serial: str):
        return post(f"{cls.url}/start", params={"serial": serial})

    @classmethod
    def stop(cls):
        return post(f"{cls.url}/stop")

    @classmethod
    def status(cls) -> bool:
        return get(f"{cls.url}/").text == "true"
