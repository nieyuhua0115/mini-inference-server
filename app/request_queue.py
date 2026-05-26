import asyncio
from dataclasses import dataclass

from app.model_runner import ModelRunner


@dataclass(frozen=True)
class PredictionJob:
    input: str
    future: asyncio.Future[str]


class PredictionQueue:
    def __init__(self, model_runner: ModelRunner) -> None:
        self._model_runner = model_runner
        self._queue: asyncio.Queue[PredictionJob | None] | None = None
        self._worker_task: asyncio.Task[None] | None = None

    async def start(self) -> None:
        if self._worker_task is not None and not self._worker_task.done():
            return

        self._queue = asyncio.Queue()
        self._worker_task = asyncio.create_task(self._worker())

    async def stop(self) -> None:
        if self._queue is None or self._worker_task is None:
            return

        await self._queue.put(None)
        await self._worker_task
        self._queue = None
        self._worker_task = None

    async def predict(self, input: str) -> str:
        if self._queue is None or self._worker_task is None or self._worker_task.done():
            raise RuntimeError("PredictionQueue is not started")

        loop = asyncio.get_running_loop()
        future: asyncio.Future[str] = loop.create_future()
        await self._queue.put(PredictionJob(input=input, future=future))
        return await future

    async def _worker(self) -> None:
        if self._queue is None:
            raise RuntimeError("PredictionQueue is not started")

        queue = self._queue
        while True:
            job = await queue.get()
            try:
                if job is None:
                    return

                try:
                    output = self._model_runner.predict(job.input)
                except Exception as exc:
                    job.future.set_exception(exc)
                else:
                    job.future.set_result(output)
            finally:
                queue.task_done()
